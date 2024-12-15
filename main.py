# MODULES
import pygame

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
pX = 128   # player starting position
pY = scrH - floorH - pW   # player is on a floor
pStepSize = 32
pFramePerStep = 10
pFrameCount = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_moving = False
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/Bill/standing.png"))
        self.sprites.append(pygame.image.load("Images/Bill/running_1.png"))
        self.sprites.append(pygame.image.load("Images/Bill/running_2.png"))
        # Initial player sprite
        self.current = 0
        self.image = self.sprites[self.current]
        # Initial player position
        self.rect = self.image.get_rect()
        self.rect.topleft = (pX, pY)
        # Initial player direction and movement
        self.is_facing_left = False
        self.is_moving = False
        self.step = 0

    def move(self, keys):
        self.is_moving = True
        if keys[pygame.K_d] and pX < scrW-self.rect.w:
            print("Key D pressed")
            self.step = pStepSize
            self.is_facing_left = False
        elif keys[pygame.K_a] and pX > 0:
            print("Key A pressed")
            self.step = -pStepSize
            self.is_facing_left = True
        else:
            self.step = 0
            self.is_moving = False

    def update(self):
        global pX
        global pFrameCount
        pFrameCount = (pFrameCount % pFramePerStep) + 1
        if self.is_moving:
            print("Player is moving")
            if pFrameCount == 2:
                self.current = (self.current % 2) + 1
                pX += self.step
            print(f"Player frame count = {pFrameCount}\nPlayer Sprite no. = {self.current}")
            self.image = self.sprites[self.current]   # update player image
        if self.is_facing_left:
            print("Player facing left.")
            self.image = pygame.transform.flip(self.sprites[self.current], True, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pX, pY)

"""pSprites = []
pSprites += [pygame.image.load("Images/Bill/standing.png")]
pSprites += [pygame.image.load("Images/Bill/running_1.png")]
pSprites += [pygame.image.load("Images/Bill/running_1.png")]
print(pSprites)
pW = 128   # Sprite width
pH = 128   # Sprite height
pX = 128   # player starting position
pY = scrH - floorH - pW   # player is on a floor
pV = 0
pFacingLeft = False
pMoving = False
pCurr = 0
pSprite = pSprites[pCurr]
framePerStep = 10
fCount = 1

def player(keys):
    global pSprite, pX, pV, pFacingLeft, pMoving, pCurr
    global framePerStep, fCount
    # Player movement
    pMoving = True
    if keys[pygame.K_a] and pX > 0:
        pFacingLeft = True
        pV = -4
    if keys[pygame.K_d] and pX < scrW - pW:
        pFacingLeft = False
        pV = 4
    else:
        pV = 0
        pMoving = False
    print(pMoving)
    # Player animation
    if pMoving:
        fCount = (fCount // framePerStep) + 1
        if fCount==2:
            pCurr = (pCurr // 2) + 1
            pX += pV
    if pFacingLeft:
        pSprite = pygame.transform.flip(pSprites[pCurr], True, False)
    else:
        pSprite = pSprites[pCurr]
    screen.blit(pSprite, (pX, pY))"""

charactersGroup = pygame.sprite.Group()

player = Player()
charactersGroup.add(player)

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

def enemy_activate():
    pass

# GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit condition
            running = False
        else:
            pass
    keys_down = pygame.key.get_pressed()
    player.move(keys_down)

    screen.fill((0, 0, 0))  # default black background
    background(0)  # game background

    charactersGroup.update()
    charactersGroup.draw(screen)
    """keysEvent = pygame.key.get_pressed()
    player(keysEvent)"""
    clock.tick(30)   # frame rate
    pygame.display.flip()  # update game screen

pygame.quit()