import pygame

import constants
from character import Character
from weapon import Weapon

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

#helper function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#load weapon images and fireball
wand_image = scale_image(pygame.image.load("assets/components/weapons/wand.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_image(pygame.image.load("assets/components/weapons/fireball.png").convert_alpha(), constants.WEAPON_SCALE)

#load mage images
mob_animation = []
mob_types = ['mage', 'orc', 'soul', 'doctor', 'thief', 'wood', 'monstro']

# create player
animation_types = ['idle', 'run']
for mob in mob_types:
    # load images
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/components/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_image(img, constants.PLAYER_SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animation.append(animation_list)

# create Character
player = Character(100, 100, mob_animation, 0)

# create weapon
wand = Weapon(wand_image, fireball_image)

#create sprite group
fireball_group = pygame.sprite.Group()

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
    fireball = wand.update(player)
    if fireball:
        fireball_group.add(fireball)

    # draw player layer
    player.draw(screen)
    wand.draw(screen)
    for fireball in fireball_group:
        fireball.draw(screen)

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
