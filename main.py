# main.py
import pygame
import constants
from character import Character
from items import Item
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon RPG")

# Clock to maintain FPS
clock = pygame.time.Clock()

# Player movement flags
move_left = False
move_right = False
move_up = False
move_down = False

# Font
font = pygame.font.Font("assets/fonts/ColleenAntics.ttf", 20)

# Helper function to scale images
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

# Load hearts (HP indicators)
heart_empty = scale_image(pygame.image.load("assets/components/heart/heart-empty.png").convert_alpha(), constants.HEART_SCALE)
heart_half  = scale_image(pygame.image.load("assets/components/heart/heart-half.png").convert_alpha(),  constants.HEART_SCALE)
heart_full  = scale_image(pygame.image.load("assets/components/heart/heart-full.png").convert_alpha(),  constants.HEART_SCALE)

# Load coin animations
coin_image = []
for i in range(4):
    img = scale_image(pygame.image.load(f"assets/components/items/coin/coin_{i}.png").convert_alpha(), constants.COIN_SCALE)
    coin_image.append(img)

# Load a potion
red_potion = scale_image(pygame.image.load("assets/components/items/heal/health-flask.png").convert_alpha(), constants.POTION_SCALE)

# Load weapon and projectile (fireball)
wand_image = scale_image(pygame.image.load("assets/components/weapons/wand.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_image(pygame.image.load("assets/components/weapons/fireball.png").convert_alpha(), constants.WEAPON_SCALE)

# Load character animations
mob_animation = []
mob_types = ['mage', 'orc', 'soul', 'doctor', 'thief', 'wood', 'monstro']
animation_types = ['idle', 'run']

for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            path = f"assets/components/characters/{mob}/{animation}/{i}.png"
            img = pygame.image.load(path).convert_alpha()
            img = scale_image(img, constants.PLAYER_SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animation.append(animation_list)

# Helper function to draw text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Display HP and score at the top panel
def draw_health_and_score(player):
    # Panel background
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    # Panel separator line
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50), 2)

    # Draw hearts
    half_drawn = False
    for i in range(5):
        # Each heart = 20 HP
        if player.health >= (i + 1) * 20:
            screen.blit(heart_full, (10 + i * 40, 0))
        elif (player.health % 20 != 0) and not half_drawn and player.health >= i * 20:
            screen.blit(heart_half, (10 + i * 40, 0))
            half_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 40, 0))

    # Draw the player's score in the top-right
    draw_text(f"x {player.score}", font, constants.RED, constants.SCREEN_WIDTH - 60, 15)

# Damage text (floating text when hitting enemies)
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Move the text upwards
        self.rect.y -= 1
        # Remove it after 30 frames
        self.counter += 1
        if self.counter > 30:
            self.kill()

# Create the player
player = Character(100, 100, 100, mob_animation, 0)
# Create an enemy
enemy = Character(300, 200, 100, mob_animation, 1)

# Create player's weapon
wand = Weapon(wand_image, fireball_image)

# Enemy list
enemy_list = []
enemy_list.append(enemy)

# Sprite groups
damage_text_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

# Create items (potion, coin, etc.)
potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(300, 200, 0, coin_image)
item_group.add(coin)

# Similar to the tutorial, add a coin to show the score visually
score_coin = Item(constants.SCREEN_WIDTH - 80, 25, 0, coin_image)
item_group.add(score_coin)

run = True
while run:
    # Maintain the framerate
    clock.tick(constants.FPS)

    # Fill the background
    screen.fill(constants.BG)

    # Calculate movement
    dx = 0
    dy = 0
    if move_right:
        dx = constants.SPEED
    if move_left:
        dx = -constants.SPEED
    if move_up:
        dy = -constants.SPEED
    if move_down:
        dy = constants.SPEED

    # Move player and update animations
    player.move(dx, dy)
    player.update()
    for enemy in enemy_list:
        enemy.update()

    # Handle weapon logic
    fireball = wand.update(player)
    if fireball:
        fireball_group.add(fireball)

    # Update each fireball
    for fball in fireball_group:
        damage, damage_pos = fball.update(enemy_list)
        # If there is damage, display floating damage text
        if damage:
            dmg_text = DamageText(damage_pos.centerx, damage_pos.centery, str(damage), constants.RED)
            damage_text_group.add(dmg_text)

    # Update the damage text group
    damage_text_group.update()

    # Update items (coins, potions)
    item_group.update(player)

    # Draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)
    # Draw player
    player.draw(screen)
    # Draw wand
    wand.draw(screen)
    # Draw fireballs
    for fball in fireball_group:
        fball.draw(screen)
    # Draw damage text
    damage_text_group.draw(screen)
    # Draw items
    item_group.draw(screen)

    # Draw the panel with HP and score
    draw_health_and_score(player)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True

        # Key releases
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

pygame.quit()
