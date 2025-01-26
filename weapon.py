import random
import pygame
import math
import constants

class Weapon():
    def __init__(self, image, fireball_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.fireball_image = fireball_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_fire = pygame.time.get_ticks()

    def update(self, player):
        fireball = None
        self.rect.center = player.rect.center

        # angle from mouse position
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = -(pos[1] - player.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # if left mouse pressed and cooldown ready
        if pygame.mouse.get_pressed()[0] and not self.fired \
                and (pygame.time.get_ticks() - self.last_fire) >= constants.FIRE_COOLDOWN:
            fireball = Fireball(
                self.fireball_image,
                self.rect.centerx,
                self.rect.centery,
                self.angle
            )
            self.fired = True
            self.last_fire = pygame.time.get_ticks()

        # reset fired if mouse not pressed
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return fireball

    def draw(self, surface):
        # rotate weapon
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(
            self.image,
            (
                self.rect.centerx - int(self.image.get_width() / 2),
                self.rect.centery - int(self.image.get_height() / 2)
            )
        )

class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        # rotate sprite
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # speed from angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)

    def update(self, enemy_list):
        damage = 0
        damage_pos = None

        # move fireball
        self.rect.x += self.dx
        self.rect.y += self.dy

        # remove if off screen
        if (self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT):
            self.kill()

        # check collision
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(
            self.image,
            (
                self.rect.centerx - int(self.image.get_width() / 2),
                self.rect.centery - int(self.image.get_height() / 2)
            )
        )
