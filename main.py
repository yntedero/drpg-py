import pygame
import constants

from character import Character

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon RPG")

#create player
player = Character(100, 100)

#game loop
run = True
while True:

    #draw player layer
    player.draw(screen)

    #even handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    pygame.display.update()