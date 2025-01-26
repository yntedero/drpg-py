import pygame
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, character_type):
        # character type like player or enemy
        self.character_type = character_type
        self.flip = False
        self.animation_list = mob_animations[character_type]
        self.frame_index = 0
        self.action = 0  # 0 is idle, 1 is run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        # track coins or similar
        self.score = 0

        # current image
        self.image = self.animation_list[self.action][self.frame_index]
        # use small 40x40 square at bottom center
        self.rect = pygame.Rect(0, 0, 40, 40)
        # put bottom center at x y
        self.rect.midbottom = (x, y)

    def move(self, dx, dy):
        # not running by default
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        # flip sprite if moving left
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False

        # control diagonal speed
        if dx != 0 and dy != 0:
            dx *= math.sqrt(2) / 2
            dy *= math.sqrt(2) / 2

        # move the square
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # check if dead
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # decide run or idle
        if self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        # update animation
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame if done
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # reset frame if action changes
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        # flip if facing left
        flipped_image = pygame.transform.flip(self.image, self.flip, False)

        # extra upward offset if type 0
        if self.character_type == 0:
            surface.blit(
                flipped_image,
                (self.rect.x, self.rect.y - constants.PLAYER_SCALE * constants.OFFSET)
            )
        else:
            surface.blit(flipped_image, self.rect)

        # draw 40x40 square
        pygame.draw.rect(surface, constants.RED, self.rect, 1)
