import pygame

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((700, 700))

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    pygame.display.update()

pygame.quit()