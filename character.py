import pygame
import constants
import math

class Character():
    def __init__(self, x, y, animation_list):
        self.flip = False
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[self.frame_index]
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        # flip image for left movement
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False
        #control diagonal movement
        if dx != 0 and dy != 0:
            dx *= math.sqrt(2) / 2
            dy *= math.sqrt(2) / 2

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        animation_cooldown = 75
        # handle animation
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect.topleft)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)