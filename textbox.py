import pygame

class TextBox:

    def __init__(self, screenSize):
        self.topLeft = (screenSize//2 - 200, screenSize//2 - 100)
        self.active = False
        self.text = ""

    def is_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def draw(self, surface):
        if self.is_active():
            rect = pygame.Rect(self.topLeft[0], self.topLeft[1], 400, 200)
            pygame.draw.rect(surface, (255, 255, 255), rect, 0)
            font = pygame.font.SysFont('Proxima Nova', 25)
            question = font.render("What number do you wish to put?", True, (0,0,0)) 
            questionRect = question.get_rect()
            questionRect.center = ((self.topLeft[0]+200), (self.topLeft[1])+50)
            surface.blit(question, questionRect)
            text = font.render(self.text, True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = ((self.topLeft[0]+200), (self.topLeft[1])+120)
            surface.blit(text, textRect)
