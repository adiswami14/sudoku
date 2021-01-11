import pygame
import board

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((700, 700))
gameBoard = board.Board().generateBoard()

for line in gameBoard: print(line)

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True


    pygame.display.update()

pygame.quit()