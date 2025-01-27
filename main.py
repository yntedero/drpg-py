import pygame
import csv
import os
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World
from button import Button

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("DRPG Python")

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
level = 1
start_game = False
pause_game = False
screen_scroll = [0, 0]

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/ColleenAntics.ttf", 25)

# helper function to scale image
def scale_img(image, scale):
  w = image.get_width()
  h = image.get_height()
  return pygame.transform.scale(image, (w * scale, h * scale))

# load button images
start_img = scale_img(pygame.image.load("assets/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("assets/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("assets/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("assets/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)

# load heart images
heart_empty = scale_img(pygame.image.load("assets/items/heart_empty.png").convert_alpha(), constants.HEALTH_SCALE)
heart_half = scale_img(pygame.image.load("assets/items/heart_half.png").convert_alpha(), constants.HEALTH_SCALE)
heart_full = scale_img(pygame.image.load("assets/items/heart_full.png").convert_alpha(), constants.HEALTH_SCALE)

# load coin images
coin_images = []
for x in range(4):
  img = scale_img(pygame.image.load(f"assets/items/coin_{x}.png").convert_alpha(), constants.COIN_SCALE)
  coin_images.append(img)

# load potion image
red_potion = scale_img(pygame.image.load("assets/items/health_flask.png").convert_alpha(), constants.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# load weapon images
wand_image = scale_img(pygame.image.load("assets/weapons/wand.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/weapons/fireball.png").convert_alpha(), constants.WEAPON_SCALE)

# load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
  tile_image = pygame.image.load(f"assets/tiles/{x}.png").convert_alpha()
  tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
  tile_list.append(tile_image)

# load character images
mob_animations = []
mob_types = ["mage", "orc", "soul", "doctor", "thief", "wood", "monstro"]

animation_types = ["idle", "run"]
for mob in mob_types:
  animation_list = []
  for animation in animation_types:
    temp_list = []
    for i in range(4):
      img = pygame.image.load(f"assets/characters/{mob}/{animation}/{i}.png").convert_alpha()
      img = scale_img(img, constants.SCALE)
      temp_list.append(img)
    animation_list.append(temp_list)
  mob_animations.append(animation_list)

# function for displaying text on the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

# function for displaying game info
def draw_info():
  pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
  pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))

  # draw lives
  half_heart_drawn = False
  for i in range(5):
    if player.health >= ((i + 1) * 20):
      screen.blit(heart_full, (10 + i * 50, 0))
    elif (player.health % 20 > 0) and half_heart_drawn == False:
      screen.blit(heart_half, (10 + i * 50, 0))
      half_heart_drawn = True
    else:
      screen.blit(heart_empty, (10 + i * 50, 0))

  # show level
  draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 12)
  # show score
  draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 55, 12)

# function to reset level
def reset_level():
  damage_text_group.empty()
  skill_group.empty()
  item_group.empty()
  fireball_group.empty()

  data = []
  for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    data.append(r)

  return data

# damage text class
class DamageText(pygame.sprite.Sprite):
  def __init__(self, x, y, damage, color):
    pygame.sprite.Sprite.__init__(self)
    self.image = font.render(damage, True, color)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.counter = 0

  def update(self):
    # reposition based on screen scroll
    self.rect.x += screen_scroll[0]
    self.rect.y += screen_scroll[1]

    # move damage text up
    self.rect.y -= 1
    self.counter += 1
    if self.counter > 30:
      self.kill()

# prepare level data
world_data = []
for row in range(constants.ROWS):
  r = [-1] * constants.COLS
  world_data.append(r)

def load_level_data(level_number):
  file_path = f"levels/level{level_number}_data.csv"
  if not os.path.exists(file_path):
    return None  # indicates no file found

  data = []
  with open(file_path, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
      row_data = []
      for tile in row:
        row_data.append(int(tile))
      data.append(row_data)
  return data

# load the initial level
initial_data = load_level_data(level)
if initial_data is None:
  # if there's no CSV at all for the first level, exit or do something
  run = False
else:
  # fill world_data from initial_data
  for x, row in enumerate(initial_data):
    for y, tile in enumerate(row):
      world_data[x][y] = tile

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

# create player
player = world.player

# create player's weapon
wand = Weapon(wand_image, fireball_image)

# extract enemies
enemy_list = world.character_list

# create sprite groups
damage_text_group = pygame.sprite.Group()
skill_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 70, 24, 0, coin_images, True)
item_group.add(score_coin)
for item in world.item_list:
  item_group.add(item)

# create buttons
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

# main game loop
run = True
while run:

  # maintain frame rate
  clock.tick(constants.FPS)

  if not start_game:
    screen.fill(constants.MENU_BG)
    if start_button.draw(screen):
      start_game = True
    if exit_button.draw(screen):
      run = False
  else:
    if pause_game:
      screen.fill(constants.MENU_BG)
      if resume_button.draw(screen):
        pause_game = False
      if exit_button.draw(screen):
        run = False
    else:
      screen.fill(constants.BG)

      if player and player.alive:
        # calculate player movement
        dx = 0
        dy = 0
        if moving_right:
          dx = constants.SPEED
        if moving_left:
          dx = -constants.SPEED
        if moving_up:
          dy = -constants.SPEED
        if moving_down:
          dy = constants.SPEED

        # move player
        screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)

        # update world and all objects
        world.update(screen_scroll)
        for enemy in enemy_list:
          fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
          if fireball:
            fireball_group.add(fireball)
          if enemy.alive:
            enemy.update()
        player.update()

        skill = wand.update(player)
        if skill:
          skill_group.add(skill)

        for skill in skill_group:
          damage, damage_pos = skill.update(screen_scroll, world.obstacle_tiles, enemy_list)
          if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)

        damage_text_group.update()
        fireball_group.update(screen_scroll, player)
        item_group.update(screen_scroll, player)

      # draw world and entities
      world.draw(screen)
      for enemy in enemy_list:
        enemy.draw(screen)
      if player:
        player.draw(screen)
      wand.draw(screen)
      for skill in skill_group:
        skill.draw(screen)
      for fireball in fireball_group:
        fireball.draw(screen)
      damage_text_group.draw(screen)
      item_group.draw(screen)
      draw_info()
      score_coin.draw(screen)

      # check if level is done
      if player and level_complete:
        level += 1

        # try to load next CSV
        next_data = load_level_data(level)
        if next_data is None:
          # no more levels; exit game gracefully
          run = False
        else:
          # reset and load next level
          world_data = reset_level()
          for x, row in enumerate(next_data):
            for y, tile in enumerate(row):
              world_data[x][y] = tile

          world = World()
          world.process_data(world_data, tile_list, item_images, mob_animations)

          # keep player's stats
          temp_hp = player.health
          temp_score = player.score

          player = world.player
          player.health = temp_hp
          player.score = temp_score

          enemy_list = world.character_list

          score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
          item_group.add(score_coin)
          for item in world.item_list:
            item_group.add(item)

      # if player died
      if player and not player.alive:
        # show death screen
        if restart_button.draw(screen):
          world_data = reset_level()

          # reload the same level from CSV (or keep the same level number)
          same_data = load_level_data(level)
          if same_data is None:
            # if we can't load it, just exit
            run = False
          else:
            for x, row in enumerate(same_data):
              for y, tile in enumerate(row):
                world_data[x][y] = tile

            world = World()
            world.process_data(world_data, tile_list, item_images, mob_animations)

            # keep the old score
            temp_score = player.score

            player = world.player
            player.score = temp_score
            enemy_list = world.character_list

            score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
            item_group.add(score_coin)
            for item in world.item_list:
              item_group.add(item)

  # event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    # keyboard presses
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_right = True
      if event.key == pygame.K_w:
        moving_up = True
      if event.key == pygame.K_s:
        moving_down = True
      if event.key == pygame.K_ESCAPE:
        pause_game = True

    # keyboard button released
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_right = False
      if event.key == pygame.K_w:
        moving_up = False
      if event.key == pygame.K_s:
        moving_down = False

  pygame.display.update()

pygame.quit()
d