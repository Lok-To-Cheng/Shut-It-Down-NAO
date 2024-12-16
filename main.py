# MODULES
import pygame
import random

from pygame import K_SPACE

# INITIALISE
pygame.init()   # initialise pygame
clock = pygame.time.Clock()

# Game Screen
scrW, scrH = 1024, 576   # screen dimensions
screen = pygame.display.set_mode((scrW, scrH))   # create game screen (W,H)

# Title and icon
pygame.display.set_caption("Shut It Down NAO")   # title
icon = pygame.image.load("icon/NAO Icon.png")   # icon
pygame.display.set_icon(icon)

# Background Image
lvl0ImgSrc = pygame.image.load("Images/Level 0.png")
lvl0ImgSrcH = lvl0ImgSrc.get_height()
hRatio = scrH / lvl0ImgSrcH
lvl0Img = pygame.transform.scale_by(lvl0ImgSrc, hRatio)

def background(lvl):
    if lvl == 0: screen.blit(lvl0Img, (0, 0))   # Level 0 background

# Floor
floorH = 64

# Gravity
gravity = 1

# Player
pW, pH = 128, 128   # Sprite dimensions

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_moving = False
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/Bill/standing.png").convert_alpha())
        self.sprites.append(pygame.image.load("Images/Bill/running_1.png").convert_alpha())
        self.sprites.append(pygame.image.load("Images/Bill/running_2.png").convert_alpha())
        # Initial player sprite image
        self.current = 0
        self.image = self.sprites[self.current]
        # Player position
        self.x = 128
        self.y = scrH - floorH - pH
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        # Player direction and motion
        self.is_facing_left = False
        self.is_moving = False
        # Player movement and velocity
        self.x_vel = 32
        self.step = 0
        self.frame_per_step = 5
        self.frame_count = 0
        # Initial player hitbox
        self.hitbox = pygame.rect.Rect(self.x + 48, self.y + 16, 32, 112)

    def move(self, keys):
        self.is_moving = True
        if keys[pygame.K_d] and self.x < scrW-self.rect.w:
            self.step = self.x_vel
            self.is_facing_left = False
        elif keys[pygame.K_a] and self.x > 0:
            self.step = -self.x_vel
            self.is_facing_left = True
        else:
            self.step = 0
            self.is_moving = False

    def shoot(self):
        return Bullet(self.x, self.y, self.is_facing_left)

    def is_hit(self):
        for e in enemies:
            if self.hitbox.x < e.hitbox.x < (self.hitbox.x + self.hitbox.w):
                return True

    def update(self):
        self.frame_count = (self.frame_count % self.frame_per_step) + 1
        # Update player position
        if self.is_moving:
            if self.frame_count == 2:   # 2 frame delay before moving
                self.current = (self.current % 2) + 1
                self.x += self.step
        else:
            self.current = 0
        # Update player sprite image
        self.image = self.sprites[self.current]
        if self.is_facing_left:
            self.image = pygame.transform.flip(self.sprites[self.current], True, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        # Update player health points
        if self.is_hit():
            print("Bill: Ouch!")
        # Update player hitbox
        self.hitbox = pygame.rect.Rect(self.x + 48, self.y + 16, 32, 112)

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/bullets/staple.png").convert_alpha())
        self.image = self.sprites[0]
        # shooting point
        if facing_left:
            self.image = pygame.transform.flip(self.sprites[0], True, False)
            self.x_vel = -16
            self.x = x + 16
        else:
            self.x_vel = 16
            self.x = x + 112
        self.y_vel = 0
        self.y_acc = gravity   # gravitational acceleration
        self.y = y + 40
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.rect.x += self.x_vel
        self.y_vel += self.y_acc
        if self.rect.y < scrH - floorH: self.rect.y += self.y_vel
        else: self.kill()


# Enemy
eW, eH = 64, 64

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_moving = False
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/NAO/marching_1.png").convert_alpha())
        self.sprites.append(pygame.image.load("Images/NAO/marching_2.png").convert_alpha())
        # Initial enemy sprite
        self.current = 0
        self.image = self.sprites[self.current]
        # Enemy position
        self.x = random.randint(384, scrW-eW)
        self.y = scrH - floorH - eH
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        # Enemy movement
        self.x_vel = 16
        self.step = -self.x_vel
        self.frame_per_step = 5
        self.frame_count = 0
        # Initial enemy hitbox
        self.hitbox = pygame.rect.Rect(self.x + 12, self.y, 40, 64)

    def update(self):
        self.frame_count = (self.frame_count % self.frame_per_step) + 1
        if self.frame_count == 2:
            # Update enemy sprite image
            self.current = (self.current + 1) % 2
            self.image = self.sprites[self.current]
            # Update enemy position
            if self.x > 64:
                self.x += self.step
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            # Update enemy hitbox
            self.hitbox = pygame.rect.Rect(self.x + 12, self.y, 40, 64)

movingSprites = pygame.sprite.Group()
characterSprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
movingSprites.add(player)
characterSprites.add(player)

for i in range(5):
    enemy = Enemy()
    movingSprites.add(enemy)
    characterSprites.add(enemy)
    enemies.add(enemy)

# GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit condition
            running = False
        else:
            pass
    keys_down = pygame.key.get_pressed()
    player.move(keys_down)   # user input into player movement
    if keys_down[K_SPACE]:
        staple = player.shoot()
        movingSprites.add(staple)
        bullets.add(staple)

    screen.fill((0, 0, 0))   # default black background
    background(0)   # game background

    movingSprites.update()   # update sprites
    movingSprites.draw(screen)   # draw sprites

    clock.tick(30)   # frame rate
    pygame.display.flip()  # update game screen

pygame.quit()