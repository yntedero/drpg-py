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

        # calculate the angle between the player and the mouse cursor
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = -(pos[1] - player.rect.centery) # negative because pygame y coordinates increase down the screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_fire) >= constants.FIRE_COOLDOWN:
            fireball = Fireball(self.fireball_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_fire = pygame.time.get_ticks()
        # reset mouse click
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False
        return fireball

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))


class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # calculate y and x speed based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED) # negative because pygame y coordinates increase down the screen

    def update(self):
        # reposition the fireball based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy

        # check if the fireball has gone off screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))