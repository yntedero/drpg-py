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

        # Calculate the angle between the player and the mouse cursor
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = -(pos[1] - player.rect.centery)  # negative because pygame's y-increases down
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # Check for mouse click (left button) to fire
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

        # Reset the "fired" state if button is not held
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return fireball

    def draw(self, surface):
        # Rotate the weapon image based on angle
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
        # Rotate the fireball sprite
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Calculate speed on X/Y based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)

    def update(self, enemy_list):
        # Variables for damage
        damage = 0
        damage_pos = None

        # Move the fireball
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove if it goes off screen
        if (self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT):
            self.kill()

        # Check collision with any enemy
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                # Calculate random damage
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
