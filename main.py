import pygame
import pygame_gui as gui
import numpy as np
from textbox import TextBox
from board import Board

screenSize = 700
boardHeight = screenSize-100
boardRatio = screenSize/boardHeight
topLeftCorner = (50, 50)
white = (255, 255, 255)
interval = boardHeight/9 #interval value for the drawing of lines
boardSize = 81
pos = 0
scaledPos = 0
wrongPositions = []

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((screenSize, screenSize))
completedBoard = Board().getCompletedBoard()
gameBoard = Board().generateBoard()
textBox = TextBox(screenSize)

for line in completedBoard:
    print(line)

print()

for line in gameBoard:
    print(line)

def drawStyleRect(surface):
    fillColor = (50, 50, 75)
    pygame.draw.rect(screen, fillColor, (topLeftCorner[0],topLeftCorner[1],boardHeight,boardHeight), 0)
    for i in range(4):
        pygame.draw.rect(screen, white, (topLeftCorner[0]-i,topLeftCorner[1]-i,boardHeight,boardHeight), 1)

def drawMainLines(surface): 
    for i in range(9):
        topCoord = (topLeftCorner[0]+interval*i, topLeftCorner[1])
        bottomCoord = (topLeftCorner[0]+interval*i, topLeftCorner[1]+boardHeight)
        leftCoord = (topLeftCorner[0], topLeftCorner[1]+interval*i)
        rightCoord = (topLeftCorner[0]+boardHeight, topLeftCorner[1]+interval*i) 
        thickness = 1
        if i%3 == 0:
            thickness = 2 #thicker lines on edges of 3x3 sub-boards
        pygame.draw.line(screen, white, topCoord, bottomCoord, thickness)
        pygame.draw.line(screen, white, leftCoord, rightCoord, thickness)

def drawNumbers(surface):
    font = pygame.font.SysFont('Proxima Nova', 25)
    rectList = []
    for line in gameBoard:
        yInt = gameBoard.index(line)
        for i in range(0, len(line)):
            num = line[i]
            if num == 0:
                text = font.render("", True, white) #Empty string
                rectList.append(pygame.Rect((topLeftCorner[0]+interval*i)+2, (topLeftCorner[1]+interval*yInt)+2, interval-2, interval-2))
            elif [yInt, i] in wrongPositions:
                text = font.render(str(num), True, (255,0,0))
                rectList.append(pygame.Rect((topLeftCorner[0]+interval*i)+2, (topLeftCorner[1]+interval*yInt)+2, interval-2, interval-2))
            else:
                text = font.render(str(num), True, white)

            textRect = text.get_rect()
            textRect.center = ((topLeftCorner[0]+interval*i)+interval//2, (topLeftCorner[1]+interval*yInt)+interval//2)
            surface.blit(text, textRect)
    return rectList

def editGameBoard(pos):
    x = int(round(pos[1]))//boardSize
    y = int(round(pos[0]))//boardSize
    if not (x >= len(gameBoard) or y>= len(gameBoard)):
        num = int(inputNumber())
        if num>0 and num<=9:
            if gameBoard[x][y] == 0 or [x,y] in wrongPositions:
                gameBoard[x][y] = num
                if num == completedBoard[x][y]:
                    if [x,y] in wrongPositions:
                        wrongPositions.remove([x,y])
                else:
                    wrongPositions.append([x,y])


def inputNumber():
    return textBox.get_text()

gameOver = False
while not gameOver:
    drawStyleRect(screen)
    drawMainLines(screen)
    list = drawNumbers(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        
        elif event.type == pygame.KEYDOWN:
            if textBox.is_active():
                if event.unicode.isnumeric():
                    textBox.set_text(textBox.get_text()+str(event.unicode))
                elif event.key == pygame.K_RETURN:
                    textBox.set_active(False)
                    editGameBoard(tuple(np.subtract(scaledPos, topLeftCorner))) #subtract from top left corner to account for that offset
                    textBox.set_text("")
                elif event.key == pygame.K_BACKSPACE:
                    textBox.set_text(textBox.get_text()[:-1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if not textBox.is_active():
                pos = pygame.mouse.get_pos()
                scaledPos = tuple(boardRatio*np.array(pos)) #scale position to account for fact that screen is larger than board
            textBox.set_active(True)

    hoverPos = pygame.mouse.get_pos()
    for rect in list:
        if(rect.collidepoint(hoverPos)):
            pygame.draw.rect(screen, (15, 100, 15), rect, 0)
    textBox.draw(screen)
    pygame.display.update()

pygame.quit()