import pygame
import constants
import math

class Character():
    def __init__(self, x, y, mob_animations, character_type):
        self.character_type = character_type
        self.flip = False
        self.animation_list = mob_animations[character_type]
        self.frame_index = 0
        self.action = 0 # 0 = idle, 1 = run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
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
        #check what action the mage is doing 1 = run, 0 = idle
        if self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 100
        # handle animation
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check if new action different from the previous action
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        # draw character image to the screen at the rect location
        if self.character_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.PLAYER_SCALE * constants.OFFSET))
        else:
            surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)