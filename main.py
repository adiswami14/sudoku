import pygame
import board

screenSize = 700
boardHeight = screenSize-100
topLeftCorner = (50, 50)
white = (255, 255, 255)
interval = boardHeight/9

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
            thickness = 2
        pygame.draw.line(screen, white, topCoord, bottomCoord, thickness)
        pygame.draw.line(screen, white, leftCoord, rightCoord, thickness)

def drawInitialNumbers(surface):
    font = pygame.font.SysFont('Proxima Nova', 25)
    for line in gameBoard:
        yInt = gameBoard.index(line)
        for i in range(0, len(line)):
            num = line[i]
            text = font.render(str(num), True, white)
            textRect = text.get_rect()
            textRect.center = ((topLeftCorner[0]+interval*i)+interval//2, (topLeftCorner[1]+interval*yInt)+interval//2)
            surface.blit(text, textRect)

for line in gameBoard: print(line)

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    drawStyleRect(screen)
    drawMainLines(screen)
    drawInitialNumbers(screen)
    pygame.display.update()

pygame.quit()