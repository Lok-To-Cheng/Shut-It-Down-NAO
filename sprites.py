import pygame
import random
import numpy as np
from config import *
from functions import *
from font import *

class Background(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no=None):
        self.no = lvl_no
        self.game = game
        self._layer = BG_LAYER
        self.groups = [self.game.all_sprites, self.game.backgrounds]
        for group in self.groups:
            pygame.sprite.Sprite.__init__(self, group)
        if lvl_no is not None:
            self.path = f"Images/Level/{lvl_no}/background.png"
        else: self.path = "Images/MCS.png"
        image_src = pygame.image.load(self.path).convert_alpha()
        src_height = image_src.get_height()
        height_ratio = SCREEN_HEIGHT // src_height
        self.image = pygame.transform.scale_by(image_src, height_ratio)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no):
        self.game = game
        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.group)   # add new Player to all_sprites
        # Current game level
        self.level = lvl_no
        # Player sprite dimension and position
        self.width = PLAYER_WIDTH[self.level]
        self.height = PLAYER_HEIGHT[self.level]
        self.x = PLAYER_X[self.level]
        self.y = PLAYER_Y[self.level]
        self.spritesheet = pygame.image.load("Images/Player/Bill.png").convert_alpha()
        height_ratio = self.height // self.spritesheet.get_height()
        self.spritesheet = pygame.transform.scale_by(self.spritesheet, height_ratio)
        sprite_count = self.spritesheet.get_width() // self.width
        self.sprites = []
        for i in range(sprite_count):
            sprite_image = clip(self.spritesheet, self.width * i, 0, self.width, self.height)
            self.sprites.append(sprite_image)
        self.current = 0
        self.image = self.sprites[self.current]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Player direction and motion
        self.is_facing_left = False
        self.is_moving = False
        # Player movement and velocity
        self.step = PLAYER_STEP_SIZE[self.level]
        self.x_vel = 0
        self.frame_per_step = PLAYER_FRAMEPERSTEP
        self.frame_delay = 0
        # Player hitbox and health
        self.hitbox = self.rect.inflate(PLAYER_HITBOX_SHRINK[self.level])
        self.hitbox.center = np.add(self.rect.center, PLAYER_SPRITE_OFFSET[self.level])
        self.hp = 10
        self.staple_hue = 0

    def update(self):
        self.move()
        self.frame_delay = (self.frame_delay % self.frame_per_step) + 1   # frame delay before moving
        # Update player position
        if self.frame_delay == self.frame_per_step:
            if self.is_moving:
                self.current = (self.current % 2) + 1   # loop running animation
                scrolling = self.game.scroll(self.x_vel)
                if not scrolling:
                    self.x += self.x_vel
            else:
                self.current = 0
            self.shoot()
        # Update player sprite image
        if self.is_facing_left:
            self.image = pygame.transform.flip(self.sprites[self.current], True, False)
        else: self.image = self.sprites[self.current]
        # Update player health points
        if self.is_hit():
            self.hp -= 1
            self.image = self.damaged()
        if self.hp <= 0:
            self.kill()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Update player hitbox
        self.hitbox = self.rect.inflate(PLAYER_HITBOX_SHRINK[self.level])
        self.hitbox.center = np.add(self.rect.center, PLAYER_SPRITE_OFFSET[self.level])

    def move(self):
        keys = pygame.key.get_pressed()
        self.x_vel = 0
        self.is_moving = False
        if keys[pygame.K_d] and self.x < SCREEN_WIDTH - self.rect.w:
            self.x_vel = self.step
            self.is_facing_left = False
            self.is_moving = True
        if keys[pygame.K_a] and self.x > 0:
            self.x_vel = -self.step
            self.is_facing_left = True
            self.is_moving = True

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            shooting_point_x = self.x
            shooting_point_y = self.y
            if self.is_facing_left:
                shooting_point_x += PLAYER_SHOOTING_POINT_X_LEFT[self.level]
            else:
                shooting_point_x += PLAYER_SHOOTING_POINT_X_RIGHT[self.level]
            shooting_point_y += PLAYER_SHOOTING_POINT_Y[self.level]
            staple = Bullet(self.game, self.level, self, shooting_point_x, shooting_point_y, self.staple_hue)
            self.game.all_sprites.add(staple)
            self.game.attacks.add(staple)
            self.staple_hue = (self.staple_hue + 10) % 360

    def is_hit(self):
        pass

    def damaged(self):
        damaged_sprite = apply_colour(self.image, RED)
        return damaged_sprite

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no, shooter, x, y, hue):
        self.game = game
        self._layer = BULLETS_LAYER
        self.groups = [self.game.all_sprites, self.game.attacks]
        for group in self.groups:
            pygame.sprite.Sprite.__init__(self, group)
        self.level = lvl_no
        self.width = BULLET_WIDTH[self.level]
        self.height = BULLET_HEIGHT[self.level]
        if type(shooter)==Player:
            self.image_src = pygame.image.load("Images/bullets/staple.png")
        else: pass
        # Bullet position, direction, and speed
        self.image = pygame.transform.scale(self.image_src, (self.width, self.height))
        self.x = x
        self.y = y
        if shooter.is_facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x -= self.width
            self.x_vel = -BULLET_X_SPEED[self.level]
        else: self.x_vel = BULLET_X_SPEED[self.level]
        self.y_vel = 0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Bullet colour
        self.hue = hue
        self.colour = pygame.Color(0)
        self.colour.hsla = (self.hue, 100, 80, 100)
        self.image = apply_colour(self.image, self.colour)

    def update(self):
        self.rect.x += self.x_vel
        self.y_vel += GRAVITY[self.level]
        if self.rect.y < SCREEN_HEIGHT - FLOOR[self.level]:
            self.rect.y += self.y_vel
        else: self.kill()

# Basic Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no):
        self.game = game
        self._layer = ENEMIES_LAYER
        self.groups = [self.game.all_sprites, self.game.enemies]
        for group in self.groups:
            pygame.sprite.Sprite.__init__(self, group)  # add new Player to all_sprites
        self.level = lvl_no
        # Enemy sprite dimension and position
        self.width = ENEMY_WIDTH[self.level]
        self.height = ENEMY_HEIGHT[self.level]
        if self.level == 0:
            self.x = random.randint(400, SCREEN_WIDTH - ENEMY_WIDTH)
        else: self.x = SCREEN_WIDTH
        self.y = ENEMY_Y[self.level]
        self.is_moving = False
        self.spritesheet = pygame.image.load("Images/Enemy/NAO.png").convert_alpha()
        height_ratio = self.height // self.spritesheet.get_height()
        self.spritesheet = pygame.transform.scale_by(self.spritesheet, height_ratio)
        sprite_count = self.spritesheet.get_width() // self.width
        self.sprites = []
        for i in range(sprite_count):
            sprite_image = clip(self.spritesheet, self.width * i, 0, self.width, self.height)
            self.sprites.append(sprite_image)
        self.current = 0
        self.image = pygame.transform.scale(self.sprites[self.current], (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Update enemy hitbox
        self.hitbox = self.rect.inflate(PLAYER_HITBOX_SHRINK[self.level])
        self.hitbox.center = np.add(self.rect.center, PLAYER_SPRITE_OFFSET[self.level])

    def is_hit(self):
        pass

    def damaged(self):
        pass

    def update(self):
        pass

class Button:
    def __init__(self, x, y, width, height, colour, content=None, text_colour=WHITE, font_scale=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        if content is not None:
            self.text = game_font.render(content, font_scale, text_colour)
            self.text_rect = self.text.get_rect(center=(self.width//2, self.height//2))
            self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:   # mouse is left-clicked
                return True
            return False
        return False