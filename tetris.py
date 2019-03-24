import time, random, pygame, sys


"""                                       Podłączenie muzyki                                                """
pygame.mixer.pre_init(44100,16,2,4096)
pygame.font.init()

"""                                       Rozmiary okien , klatek                                          """
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 550 # 700
BOARD_WIDTH = 12
BOARD_HEIGHT = 22   # 28
BOX_SIZE = 25
BLANK = '.'

"""                                 Tworzenie zmiennych używanych w class menu                            """
WINDOW = pygame.display.set_mode((WINDOW_WIDTH*2,WINDOW_HEIGHT)) 
SCREEN = pygame.Surface((WINDOW_WIDTH*2,WINDOW_HEIGHT)) 



"""                                           Tworzenie kolorów                                           """

BLUE_TEKST  = (  0, 162, 232)
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)
ORANGE      = (255, 165,   0)
PURPLE      = (148,   0, 211)


COLORS = (BLUE,GREEN,RED,YELLOW,ORANGE,PURPLE)


"""                                           Tworzenie klockół                                          """



"""                                        KLOCKI DODANE PRZEZ MNIE                                            """


C_SHAPE = [['00',
            '0.'],
            ['00',
             '.0'],
            ['.0',
             '00'],
            ['0.',
             '00']]




"""                                           STANDARDOWE KLOCKI                                           """




S_SHAPE = [['.00',
            '00.',],
          ['0.',
           '00',
           '.0',]]

Z_SHAPE = [['00.',
            '.00',],
          [ '.0',
            '00',
            '0.',]]

I_SHAPE = [['0',
            '0',
            '0',
            '0'],
          ['0000']]

O_SHAPE = [['00',
            '00']]

J_SHAPE = [['0..',
            '000'],
            ['00',
             '0.',
             '0.'],
            ['000',
             '..0'],
             ['.0',
              '.0',
              '00']]

L_SHAPE = [['..0',
            '000'],
           ['0.',
            '0.',
            '00'],
           ['000',
            '0..'],
            ['00',
            '.O',
            '.0.']]

T_SHAPE = [['.0.',
            '00O'],
           ['0.',
            '00',
            '0.'],
           ['000',
            '.0.'],
           ['.0',
            '00',
            '.O']]



SHAPES = {'C': C_SHAPE,'S': S_SHAPE,'Z': Z_SHAPE,'J': J_SHAPE,'L': L_SHAPE,'I': I_SHAPE,'O': O_SHAPE,'T': T_SHAPE}



"""                      Klasa menu , z opcjami (game,quit) , tworzy się możliwosć pause podczas gry  """

class Menu(object):
    def __init__(self, punkts = [120,120,u'Punkt',WHITE,GREEN]):
        self.punkts = punkts
    
    def render(self,board, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                board.blit(font.render(i[2] , 1 , i[4]), (i[0], i[1]))
            else:
                board.blit(font.render(i[2] , 1 , i[3]), (i[0], i[1]))
    
    def menu(self):
        done = True
        font_menu = pygame.font.SysFont('Comic Sans MS' , 50)
        punkt = 0
        
        while done:
            SCREEN.fill(BLACK)
            
            self.render(SCREEN , font_menu , punkt)
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                    
                    if e.key == pygame.K_SPACE:
                        if punkt == 0:
                            
                            done = False
                        elif punkt == 1:
                            pygame.quit()
                            sys.exit()
            WINDOW.blit(SCREEN , (0,0))
            pygame.display.set_caption('Tetris')
            pygame.display.flip()
            


"""                                            Tworzenie punktów w menu , wywołanie klasy menu"""
punkts = [(230,170, u'Game',WHITE,GREEN,0),
          (230,240, u'Quit',WHITE,GREEN,1)]
game = Menu(punkts)
game.menu()


"""                                   Klasa przyznaczona dla tworzenia planszy , na której odbywa się gra """

class Board(object):
    def __init__(self):
        self.m_array = [[BLANK] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]

    def addToBoard(self, piece):
        shape = SHAPES[piece.getShapeIndex()][piece.getRotation()]
        height = len(shape)
        width = len(shape[0])

        for y in range(height):
            for x in range(width):
                if shape[y][x] != BLANK:
                    self.m_array[y + int(piece.getPosY() / BOX_SIZE)][x + int(piece.getPosX() / BOX_SIZE)] = piece.getColor()

    def draw(self, screen):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.m_array[y][x] != BLANK:
                    pygame.draw.rect(screen, COLORS[int(self.m_array[y][x])], (x * BOX_SIZE, y * BOX_SIZE, BOX_SIZE, BOX_SIZE))
                    

    def isCompleteLine(self, y):
        for x in range(BOARD_WIDTH):
            if self.m_array[y][x] == BLANK: return False
        return True

    def removeCompleteLines(self):
        y = BOARD_HEIGHT - 1
        numOfCompleteLines = 0

        while y >= 0:
            if self.isCompleteLine(y):
                numOfCompleteLines += 1
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARD_WIDTH):
                        self.m_array[pullDownY][x] = self.m_array[pullDownY - 1][x]

                for x in range(BOARD_WIDTH):
                    self.m_array[0][x] = BLANK
            else:
                y -= 1
        return numOfCompleteLines

    def get(self, x, y):
        return self.m_array[y][x]


"""                             Klasa przy pomocy której zmieniamy klocek , wykonujemy poruszanie się po planszę """

class Object(object):
    def __init__(self):
        self.m_shapeIndex = random.choice(list(SHAPES.keys()))
        self.m_position = {'x' : int(WINDOW_WIDTH + 0.5 * WINDOW_WIDTH) - 35, 'y' : WINDOW_HEIGHT / 3.5}
        self.m_color = random.randint(0, len(COLORS) - 1)
        self.m_rotation = random.randint(0, len(SHAPES[self.m_shapeIndex]) - 1)
        self.m_shape = SHAPES[self.m_shapeIndex][self.m_rotation]
        self.m_shapeHeight = len(self.m_shape)
        self.m_shapeWidth = len(self.m_shape[0])

    def getShapeIndex(self): return self.m_shapeIndex
    def getRotation(self): return self.m_rotation
    def getPosX(self): return self.m_position['x']
    def getPosY(self): return self.m_position['y']
    def getColor(self): return self.m_color

    def setPos(self, x, y):
        self.m_position['x'] = x
        self.m_position['y'] = y

    def setRotation(self, rotation):
        self.rotation = rotation

    def move(self, x, y, board):
        if self.isValidPosition(x, y, board):
            self.m_position['x'] += x
            self.m_position['y'] += y
            return True

        else: return False

    def isValidPosition(self, additionX, additionY, board):
        for y in range(self.m_shapeHeight):
            for x in range(self.m_shapeWidth):
                if self.m_shape[y][x] == BLANK: continue

                xPos = x + int((self.m_position['x'] + additionX) / BOX_SIZE)
                yPos = y + int((self.m_position['y'] + additionY) / BOX_SIZE)

                if xPos < 0 or xPos >= BOARD_WIDTH or yPos >= BOARD_HEIGHT: return False
                if board.get(xPos, yPos) != BLANK: return False

        return True

    def rotate(self, board):
        shape = SHAPES[self.m_shapeIndex][(self.m_rotation + 1) % len(SHAPES[self.m_shapeIndex])]
        width = len(shape[0])

        rotation = self.m_rotation
        shape = self.m_shape
        shapeHeight = self.m_shapeHeight
        shapeWidth = self.m_shapeWidth

        self.m_rotation = (self.m_rotation + 1) % len(SHAPES[self.m_shapeIndex])
        self.m_shape = SHAPES[self.m_shapeIndex][self.m_rotation]
        self.m_shapeHeight = len(self.m_shape)
        self.m_shapeWidth = len(self.m_shape[0])

        if (self.m_position['x'] + width * BOX_SIZE) <= WINDOW_WIDTH and self.isValidPosition(0, 0, board):
            pass
        else:
            self.m_rotation = rotation
            self.m_shape = shape
            self.m_shapeWidth = shapeWidth
            self.m_shapeHeight = shapeHeight

    def draw(self, screen):
        for y in range(self.m_shapeHeight):
            for x in range(self.m_shapeWidth):
                if self.m_shape[y][x] != BLANK:
                    pygame.draw.rect(screen, COLORS[self.m_color], (self.m_position['x'] + x * BOX_SIZE, self.m_position['y'] + y * BOX_SIZE, BOX_SIZE, BOX_SIZE))
                    



"""                              Główna klasa przez którą wypisujemy następny klocek , zdobyte punkty , rysowanie klatek"""

class Main(object):
    def __init__(self):
        self.m_board = Board()
        self.m_currPiece = None
        self.m_nextPiece = Object()
        self.m_pieceFalling = False
        self.m_gameOver = False
        self.m_direction = {'left' : False, 'right' : False, 'down' : False}
        self.m_rotate = False
        self.m_lastFallTime = time.time()
        self.m_lastMoveTime = time.time()
        self.m_score = 0

        pygame.init()
        self.m_screen = pygame.display.set_mode((WINDOW_WIDTH * 2, WINDOW_HEIGHT))
        pygame.mixer.music.load("tetris-gameboy-02.mp3")
        pygame.display.set_caption('Tetris')
        pygame.mixer.music.play(-1,2)
        
        
        

    def logic(self):
        if time.time() - self.m_lastMoveTime > 0.1:
            if self.m_direction['left'] == True:    self.m_currPiece.move(-BOX_SIZE, 0, self.m_board)
            elif self.m_direction['right'] == True: self.m_currPiece.move(BOX_SIZE, 0, self.m_board)
            elif self.m_direction['down'] == True:  self.m_currPiece.move(0, BOX_SIZE, self.m_board)

            self.m_lastMoveTime = time.time()

        elif self.m_rotate:
            self.m_currPiece.rotate(self.m_board)
            self.m_rotate = False

    def drawLines(self):
        for i in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.m_screen, WHITE, (i * BOX_SIZE, 0), (i * BOX_SIZE, WINDOW_HEIGHT))
        for j in range(BOARD_HEIGHT):
            pygame.draw.line(self.m_screen, WHITE, (0 , j * BOX_SIZE), (WINDOW_WIDTH, j * BOX_SIZE))

    def textObjects(self, text, font):
        textSurface = font.render(text, True, BLUE_TEKST)
        return textSurface, textSurface.get_rect()

    def displayScore(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        font1 = pygame.font.Font('freesansbold.ttf', 22)
        textSurf, textRect = self.textObjects('Punkty: ' + str(self.m_score), font)
        textRect.center = (WINDOW_WIDTH + 0.5 * WINDOW_WIDTH , WINDOW_HEIGHT / 1.1)
        textSurf2, textRect2 = self.textObjects('Następny klocek:', font)
        textRect2.center = (WINDOW_WIDTH + 0.5 * WINDOW_WIDTH, WINDOW_HEIGHT / 6)
        textSurf3 , textRect3 = self.textObjects("space - obracanie klocka" ,font1)
        textRect3.center = (WINDOW_WIDTH + 0.5 * WINDOW_WIDTH , WINDOW_HEIGHT / 1.6)
        self.m_screen.blit(textSurf, textRect)
        self.m_screen.blit(textSurf2, textRect2)
        self.m_screen.blit(textSurf3, textRect3)

    def draw(self):
        if self.m_gameOver: return
        self.m_screen.fill(BLACK)
        self.drawLines()
        self.m_board.draw(self.m_screen)
        self.m_currPiece.draw(self.m_screen)
        self.m_nextPiece.draw(self.m_screen)
        self.displayScore()
        pygame.display.update()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.m_gameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:     self.m_direction['left'] = True
                elif event.key == pygame.K_RIGHT:  self.m_direction['right'] = True
                elif event.key == pygame.K_DOWN:   self.m_direction['down'] = True
                elif event.key == pygame.K_SPACE:  self.m_rotate = True
                elif event.key == pygame.K_ESCAPE: 
                    pygame.mixer.music.pause()
                    game.menu()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:     self.m_direction['left'] = False
                elif event.key == pygame.K_RIGHT:  self.m_direction['right'] = False
                elif event.key == pygame.K_DOWN:   self.m_direction['down'] = False

    def update(self):
        if time.time() - self.m_lastFallTime > 1:
            if self.m_pieceFalling:
                if self.m_currPiece.move(0, BOX_SIZE, self.m_board): pass

                else:
                    self.m_pieceFalling = False
                    self.m_board.addToBoard(self.m_currPiece)
                    self.m_score += self.m_board.removeCompleteLines()*10

                self.m_lastFallTime = time.time()
        
        if not self.m_pieceFalling:
            self.m_currPiece = self.m_nextPiece
            self.m_nextPiece = Object()
            self.m_currPiece.setPos(int(WINDOW_WIDTH / 2) - 50, 0)
            self.m_pieceFalling = True
            if not self.m_currPiece.isValidPosition(0, 0, self.m_board): self.m_gameOver = True
    
    
        
    def runGame(self):
        while not self.m_gameOver:
            pygame.mixer.music.unpause()
            self.update()
            self.input()
            self.logic()
            self.draw()
        
        
        

"""                                              Tworzenie zmiennej klasy main, wywowanie gry                   """

MainGame = Main()
MainGame.runGame()
pygame.quit()