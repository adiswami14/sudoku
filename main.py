import pygame
import pygame_gui as gui
import board
import numpy as np

screenSize = 700
boardHeight = screenSize-100
boardRatio = screenSize/boardHeight
topLeftCorner = (50, 50)
white = (255, 255, 255)
interval = boardHeight/9 #interval value for the drawing of lines
boardSize = 81

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((screenSize, screenSize))
gameBoard = board.Board().generateBoard()

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
            else:
                text = font.render(str(num), True, white)

            textRect = text.get_rect()
            textRect.center = ((topLeftCorner[0]+interval*i)+interval//2, (topLeftCorner[1]+interval*yInt)+interval//2)
            s = surface.blit(text, textRect)
            rectList.append(s)
    return rectList

def editGameBoard(pos):
    x = int(round(pos[1]))//boardSize
    y = int(round(pos[0]))//boardSize
    if not (x >= len(gameBoard) or y>= len(gameBoard)):
        num = int(inputNumber())
        if num>0 and num<=9:
            gameBoard[x][y] = num


def inputNumber():
    x = input("What number do you want to input at this position? ") #TODO: Implement textbox functionality so an input field pops up
    return x

gameOver = False
while not gameOver:
    drawStyleRect(screen)
    drawMainLines(screen)
    list = drawNumbers(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            scaledPos = tuple(boardRatio*np.array(pos)) #scale position to account for fact that screen is larger than board
            editGameBoard(tuple(np.subtract(scaledPos, topLeftCorner))) #subtract from top left corner to account for that offset

    pygame.display.update()

pygame.quit()