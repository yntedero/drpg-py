import pygame

import constants
from character import Character

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon RPG")

# clock for frame rate
clock = pygame.time.Clock()

# define player movement variables
move_left = False
move_right = False
move_up = False
move_down = False


#help function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# create player
animation_list = []
for i in range(4):
    img = pygame.image.load(f"assets/components/charater/idle/{i}.png").convert_alpha()
    img = scale_image(img, constants.SCALE)
    animation_list.append(img)

player = Character(100, 100, animation_list)

# game loop
run = True
while True:

    # frame rate
    clock.tick(constants.FPS)

    # draw background
    screen.fill(constants.BG)

    # calc player movement
    dx = 0
    dy = 0
    if move_right == True:
        dx = constants.SPEED
    if move_left == True:
        dx = -constants.SPEED
    if move_up == True:
        dy = -constants.SPEED
    if move_down == True:
        dy = constants.SPEED

    # move player
    player.move(dx, dy)

    # update player animation
    player.update()

    # draw player layer
    player.draw(screen)

    # even handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        # keyboard input press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True

        # keyboard input release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s:
                move_down = False

    pygame.display.update()
