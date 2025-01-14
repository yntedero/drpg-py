import pygame
import constants

class Character():
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, (constants.RED), self.rect)