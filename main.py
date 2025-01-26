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

#define font
font = pygame.font.Font("assets/fonts/ColleenAntics.ttf", 20)

#helper function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# load health images
heart_empty = scale_image(pygame.image.load("assets/components/heart/heart-empty.png").convert_alpha(), constants.HEART_SCALE)
heart_half = scale_image(pygame.image.load("assets/components/heart/heart-half.png").convert_alpha(), constants.HEART_SCALE)
heart_full = scale_image(pygame.image.load("assets/components/heart/heart-full.png").convert_alpha(), constants.HEART_SCALE)

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

# function to draw player health
def draw_health():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50), 2)
    # draw lives
    for i in range(5):
        # draw full heart
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif player.health >= (i * 20):
            screen.blit(heart_half, (10 + i * 50, 0))
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete after a few frames
        self.counter += 1
        if self.counter > 30:
            self.kill()

# create Character
player = Character(100, 100, 100, mob_animation, 0)

# create enemy
enemy = Character(100, 100, 100, mob_animation, 1)

# create players weapon
wand = Weapon(wand_image, fireball_image)

# create empty enemy list
enemy_list = []
enemy_list.append(enemy)

#create sprite group
damage_text_group = pygame.sprite.Group()
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

    # update player
    for enemy in enemy_list:
        enemy.update()
    player.update()
    fireball = wand.update(player)
    if fireball:
        fireball_group.add(fireball)
    for fireball in fireball_group:
        fireball.update(enemy_list)
    damage_text_group.update()
    draw_health()

    # draw player on screen
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    wand.draw(screen)
    for fireball in fireball_group:
        damage, damage_pos = fireball.update(enemy_list)
        fireball.draw(screen)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.centery, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.draw(screen)

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
