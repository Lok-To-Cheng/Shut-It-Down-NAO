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
        self.groups = self.game.all_sprites, self.game.backgrounds
        pygame.sprite.Sprite.__init__(self, self.groups)
        if lvl_no is not None:
            self.path = f"Images/Level/{lvl_no}/background.png"
        else: self.path = "Images/MCS.png"
        image_src = pygame.image.load(self.path).convert_alpha()
        src_height = image_src.get_height()
        height_ratio = SCREEN_HEIGHT // src_height
        self.image = pygame.transform.scale_by(image_src, height_ratio)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.group)   # add new Player to all_sprites
        # Current game level
        self.level = self.game.level
        # Player sprite dimension and position
        self.width = PLAYER_WIDTH[self.level]
        self.height = PLAYER_HEIGHT[self.level]
        self.x = PLAYER_X[self.level]
        self.y = PLAYER_Y[self.level]
        # Player sprite images
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
        # Player hitbox and health
        self.hitbox = self.rect.inflate(PLAYER_HITBOX_SHRINK[self.level])
        self.hitbox.center = np.add(self.rect.center, PLAYER_SPRITE_OFFSET[self.level])
        self.knockback = -self.step
        self.hp = 10
        self.staple_hue = 0   # fancy staples

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
        for enemy in self.game.enemies:
            if self.hitbox.colliderect(enemy.hitbox):
                if enemy.x < self.x:
                    self.knockback = self.step
                return True
        return False

    def damaged(self):
        damaged_sprite = apply_colour(self.image, RED)
        return damaged_sprite

    def update(self):
        self.move()
        # Update player position
        if self.game.frame_delay == FRAME_DELAY:
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
            self.x += self.knockback
            self.image = self.damaged()
        if self.hp <= 0:
            self.kill()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Update player hitbox
        self.hitbox = self.rect.inflate(PLAYER_HITBOX_SHRINK[self.level])
        self.hitbox.center = np.add(self.rect.center, PLAYER_SPRITE_OFFSET[self.level])

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no, shooter, x, y, hue):
        self.game = game
        self._layer = BULLETS_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
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
        self.goes_left = False
        if shooter.is_facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x -= self.width
            self.x_vel = -BULLET_X_SPEED[self.level]
            self.goes_left = True
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
    def __init__(self, game):
        self.game = game
        self._layer = ENEMIES_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)  # add new Player to all_sprites
        self.level = self.game.level
        # Enemy sprite dimension and position
        self.width = ENEMY_WIDTH[self.level]
        self.height = ENEMY_HEIGHT[self.level]
        if self.level == 0:
            self.x = random.randint(400, SCREEN_WIDTH - self.width)
        else: self.x = random.randint(SCREEN_WIDTH, self.game.background.rect.width - self.width)
        self.y = ENEMY_Y[self.level]
        # Enemy sprite images
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
        # Enemy movement and speed
        self.step = ENEMY_STEP_SIZE[self.level]
        self.x_vel = -self.step
        # Enemy hitbox
        self.hitbox = self.rect.inflate(ENEMY_HITBOX_SHRINK[self.level])
        self.hitbox.center = self.rect.center
        self.knockback = self.step
        self.hp = 5

    def is_hit(self):
        for bullet in self.game.attacks:
            if self.hitbox.colliderect(bullet.rect):
                if bullet.goes_left:
                    self.knockback = -self.step
                return True
        return False

    def damaged(self):
        damaged_sprite = apply_colour(self.image, RED)
        return damaged_sprite

    def update(self):
        # Update enemy position
        if self.game.frame_delay == FRAME_DELAY:
            self.current = (self.current + 1) % 2  # loop marching animation
            self.x += self.x_vel
        # Update enemy sprite image
        self.image = self.sprites[self.current]
        # Update enemy health points
        if self.is_hit():
            self.hp -= 1
            self.x += self.knockback
            self.image = self.damaged()
        if self.hp <= 0:
            self.kill()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Update enemy hitbox
        self.hitbox = self.rect.inflate(ENEMY_HITBOX_SHRINK[self.level])
        self.hitbox.center = self.rect.center


class Button:
    def __init__(self, x, y, width, height, colour, content=None, text_colour=WHITE, font_scale=1, outline_colour=None, outline_width=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        # Button background
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # Button text (optional)
        if content is not None:
            self.text = game_font.render(content, font_scale, text_colour)
            self.text_rect = self.text.get_rect(center=(self.width//2, self.height//2))
            self.image.blit(self.text, self.text_rect)
        if outline_colour is not None:
            pygame.draw.rect(self.image, outline_colour, self.rect, outline_width)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:   # mouse is left-clicked
                return True
            return False
        return False