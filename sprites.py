import pygame
from config import *
from font import *

class LevelBackground(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no):
        self.no = lvl_no
        self.game = game
        self._layer = BG_LAYER
        self.groups = [self.game.all_sprites, self.game.level_backgrounds]
        for group in self.groups:
            pygame.sprite.Sprite.__init__(self, group)
        self.path = f"Images/Level/{lvl_no}/background.png"
        self.image = pygame.image.load(self.path).convert_alpha()
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, lvl_no):
        self.game = game
        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.group)   # add new Player to all_sprites
        # Player sprite dimension and position
        self.width = PLAYER_WIDTH[lvl_no]
        self.height = PLAYER_HEIGHT[lvl_no]
        self.x = PLAYER_X[lvl_no]
        self.y = PLAYER_Y[lvl_no]
        self.sprites = [pygame.image.load("Images/Bill/standing.png").convert_alpha(),
                        pygame.image.load("Images/Bill/running_1.png").convert_alpha(),
                        pygame.image.load("Images/Bill/running_2.png").convert_alpha()]
        self.current = 0
        self.image = pygame.transform.scale(self.sprites[self.current], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        # Player direction and motion
        self.is_facing_left = False
        self.is_moving = False
        # Player movement and velocity
        self.step = PLAYER_STEP_SIZE[lvl_no]
        self.x_vel = 0
        self.frame_per_step = PLAYER_FRAMEPERSTEP
        self.frame_count = 0
        # Player hitbox
        self.hitbox = pygame.rect.Rect(PLAYER_HITBOX[lvl_no])

    def update(self):
        self.frame_count = (self.frame_count % self.frame_per_step) + 1
        # Update player position
        if self.is_moving:
            if self.frame_count == 2:  # 2 frame delay before moving
                self.current = (self.current % 2) + 1  # loop running animation
                self.x += self.x_vel

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
        pass

    def is_hit(self):
        pass

    def damaged(self):
        pass

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left):
        super().__init__()

    def update(self):
        pass

# Basic Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

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