# MODULES
import pygame
import random

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
imgSrcH = lvl0ImgSrc.get_height()
hRatio = scrH / imgSrcH
lvl0Img = pygame.transform.scale_by(lvl0ImgSrc, hRatio)

def background(lvl):
    if lvl == 0: screen.blit(lvl0Img, (0, 0))   # Level 0 background
# Floor
floorH = 64

# Player
pW, pH = 128, 128   # Sprite dimensions

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_moving = False
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/Bill/standing.png"))
        self.sprites.append(pygame.image.load("Images/Bill/running_1.png"))
        self.sprites.append(pygame.image.load("Images/Bill/running_2.png"))
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
        self.xvel = 32
        self.step = 0
        self.frame_per_step = 5
        self.frame_count = 0
        # Initial player hitbox
        self.hitbox = (self.x + 48, self.y + 16, 32, 112)

    def move(self, keys):
        self.is_moving = True
        if keys[pygame.K_d] and self.x < scrW-self.rect.w:
            self.step = self.xvel
            self.is_facing_left = False
        elif keys[pygame.K_a] and self.x > 0:
            self.step = -self.xvel
            self.is_facing_left = True
        else:
            self.step = 0
            self.is_moving = False

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
        # Update player hitbox
        self.hitbox = (self.x + 48, self.y + 16, 32, 112)

# Enemy
eW, eH = 64, 64

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_moving = False
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/NAO/marching_1.png"))
        self.sprites.append(pygame.image.load("Images/NAO/marching_2.png"))
        # Initial enemy sprite
        self.current = 0
        self.image = self.sprites[self.current]
        # Enemy position
        self.x = random.randint(384, scrW-eW)
        self.y = scrH - floorH - eH
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        # Enemy movement
        self.xvel = 16
        self.step = -self.xvel
        self.frame_per_step = 5
        self.frame_count = 0
        # Initial enemy hitbox
        self.hitbox = (self.x + 12, self.y, 40, 64)

    def update(self):
        self.frame_count = (self.frame_count % self.frame_per_step) + 1
        if self.frame_count == 2:
            # Update enemy sprite image
            self.current = (self.current + 1) % 2
            self.image = self.sprites[self.current]
            # Update enemy position
            self.x += self.step
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            # Update enemy hitbox
            self.hitbox = (self.x + 12, self.y, 40, 64)

charactersGroup = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
charactersGroup.add(player)

for i in range(5):
    enemy = Enemy()
    enemies.add(enemy)
    charactersGroup.add(enemy)

# GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit condition
            running = False
        else:
            pass
    keys_down = pygame.key.get_pressed()
    player.move(keys_down)   # user input

    screen.fill((0, 0, 0))   # default black background
    background(0)   # game background

    charactersGroup.update()   # update sprites
    charactersGroup.draw(screen)   # draw sprites

    clock.tick(30)   # frame rate
    pygame.display.flip()  # update game screen

pygame.quit()