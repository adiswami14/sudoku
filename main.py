import pygame
import pygame_gui as gui
import numpy as np
from textbox import TextBox
from board import Board
from boardGenerator import BoardGenerator

SCREEN_SIZE = 700
BOARD_HEIGHT = SCREEN_SIZE-100
BOARD_RATIO = SCREEN_SIZE/BOARD_HEIGHT
TOP_LEFT_CORNER = (50, 50)
WHITE = (255, 255, 255)
INTERVAL = BOARD_HEIGHT/9 #interval value for the drawing of lines
BOARD_SIZE = 81
POS = 0
SCALED_POS = 0
WRONG_POSITIONS = []

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
font = pygame.font.SysFont('Proxima Nova', 25)

COMPLETED_BOARD = Board().getCompletedBoard()
GAME_BOARD = BoardGenerator(COMPLETED_BOARD).generateBoard()
TEXTBOX = TextBox(SCREEN_SIZE)

for line in COMPLETED_BOARD:
    print(line)

print()

for line in GAME_BOARD:
    print(line)

def drawStyleRect(surface):
    fillColor = (50, 50, 75)
    pygame.draw.rect(screen, fillColor, (TOP_LEFT_CORNER[0],TOP_LEFT_CORNER[1],BOARD_HEIGHT,BOARD_HEIGHT), 0)
    for i in range(4):
        pygame.draw.rect(screen, WHITE, (TOP_LEFT_CORNER[0]-i,TOP_LEFT_CORNER[1]-i,BOARD_HEIGHT,BOARD_HEIGHT), 1)

def drawMainLines(surface): 
    for i in range(9):
        topCoord = (TOP_LEFT_CORNER[0]+INTERVAL*i, TOP_LEFT_CORNER[1])
        bottomCoord = (TOP_LEFT_CORNER[0]+INTERVAL*i, TOP_LEFT_CORNER[1]+BOARD_HEIGHT)
        leftCoord = (TOP_LEFT_CORNER[0], TOP_LEFT_CORNER[1]+INTERVAL*i)
        rightCoord = (TOP_LEFT_CORNER[0]+BOARD_HEIGHT, TOP_LEFT_CORNER[1]+INTERVAL*i) 
        thickness = 1
        if i%3 == 0:
            thickness = 2 #thicker lines on edges of 3x3 sub-boards
        pygame.draw.line(screen, WHITE, topCoord, bottomCoord, thickness)
        pygame.draw.line(screen, WHITE, leftCoord, rightCoord, thickness)

def drawNumbers(surface):
    rectList = []
    for line in GAME_BOARD:
        yInt = GAME_BOARD.index(line)
        for i in range(0, len(line)):
            num = line[i]
            if num == 0:
                text = font.render("", True, WHITE) #Empty string
                rectList.append(pygame.Rect((TOP_LEFT_CORNER[0]+INTERVAL*i)+2, (TOP_LEFT_CORNER[1]+INTERVAL*yInt)+2, INTERVAL-2, INTERVAL-2))
            elif [yInt, i] in WRONG_POSITIONS:
                text = font.render(str(num), True, (255,0,0))
                rectList.append(pygame.Rect((TOP_LEFT_CORNER[0]+INTERVAL*i)+2, (TOP_LEFT_CORNER[1]+INTERVAL*yInt)+2, INTERVAL-2, INTERVAL-2))
            else:
                text = font.render(str(num), True, WHITE)

            textRect = text.get_rect()
            textRect.center = ((TOP_LEFT_CORNER[0]+INTERVAL*i)+INTERVAL//2, (TOP_LEFT_CORNER[1]+INTERVAL*yInt)+INTERVAL//2)
            surface.blit(text, textRect)
    return rectList

def editGameBoard(pos):
    x = int(round(pos[1]))//BOARD_SIZE
    y = int(round(pos[0]))//BOARD_SIZE
    if not (x >= len(GAME_BOARD) or y>= len(GAME_BOARD)):
        num = int(inputNumber())
        if num>0 and num<=9:
            if GAME_BOARD[x][y] == 0 or [x,y] in WRONG_POSITIONS:
                GAME_BOARD[x][y] = num
                if num == COMPLETED_BOARD[x][y]:
                    if [x,y] in WRONG_POSITIONS:
                        WRONG_POSITIONS.remove([x,y])
                else:
                    WRONG_POSITIONS.append([x,y])


def inputNumber():
    return TEXTBOX.get_text()

gameOver = False
gameWon = False
while not gameOver:
    if gameWon:
        screen.fill((0,0,0))
        text = font.render("You won!", True, WHITE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_SIZE//2, SCREEN_SIZE//2)
        screen.blit(text, textRect)
    else:
        drawStyleRect(screen)
        drawMainLines(screen)
        list = drawNumbers(screen)
        if len(list) == 0:
            gameWon = True
        hoverPos = pygame.mouse.get_pos()
        for rect in list:
            if(rect.collidepoint(hoverPos)):
                pygame.draw.rect(screen, (15, 100, 15), rect, 0)
        TEXTBOX.draw(screen)
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            
            elif event.type == pygame.KEYDOWN:
                if TEXTBOX.is_active():
                    if event.unicode.isnumeric():
                        TEXTBOX.set_text(TEXTBOX.get_text()+str(event.unicode))
                    elif event.key == pygame.K_RETURN:
                        TEXTBOX.set_active(False)
                        editGameBoard(tuple(np.subtract(SCALED_POS, TOP_LEFT_CORNER))) #subtract from top left corner to account for that offset
                        TEXTBOX.set_text("")
                    elif event.key == pygame.K_BACKSPACE:
                        TEXTBOX.set_text(TEXTBOX.get_text()[:-1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if not TEXTBOX.is_active():
                    POS = pygame.mouse.get_pos()
                    SCALED_POS = tuple(BOARD_RATIO*np.array(POS)) #scale position to account for fact that screen is larger than board
                TEXTBOX.set_active(True)
    pygame.display.update()

pygame.quit()