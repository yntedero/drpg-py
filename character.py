# character.py
import pygame
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, character_type):
        # Character type (e.g. player or enemy)
        self.character_type = character_type
        self.flip = False
        self.animation_list = mob_animations[character_type]
        self.frame_index = 0
        self.action = 0  # 0 = idle, 1 = run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        # Score tracking (coins, etc.)
        self.score = 0

        # Current image
        self.image = self.animation_list[self.action][self.frame_index]
        # Instead of stretching a rectangle over the whole sprite,
        # we create a small 40x40 square at the bottom center.
        self.rect = pygame.Rect(0, 0, 40, 40)
        # This ensures the bottom center of the square is placed at (x, y).
        self.rect.midbottom = (x, y)

    def move(self, dx, dy):
        # By default, not running
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        # Flip the sprite if moving left
        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False

        # Control diagonal speed
        if dx != 0 and dy != 0:
            dx *= math.sqrt(2) / 2
            dy *= math.sqrt(2) / 2

        # Update the square's position
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # Check if the character is dead
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # Determine if character is running or idle
        if self.running:
            self.update_action(1)  # 1 = run
        else:
            self.update_action(0)  # 0 = idle

        # Handle animation
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Reset the frame index if animation is over
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # If the action changed, reset the frame index
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        # Flip image if character is facing left
        flipped_image = pygame.transform.flip(self.image, self.flip, False)

        # If this is the main character (type 0), apply an extra upward offset
        # so the sprite is drawn above the square.
        if self.character_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.PLAYER_SCALE * constants.OFFSET)
            )
        else:
            surface.blit(flipped_image, self.rect)

        # Draw only the small 40x40 square at the bottom center for debugging
        pygame.draw.rect(surface, constants.RED, self.rect, 1)
