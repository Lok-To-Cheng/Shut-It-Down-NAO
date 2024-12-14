import pygame
pygame.init()   # initialise pygame

scrW = 1024
scrH = 576
screen = pygame.display.set_mode([scrW, scrH])   # create game screen [W,H]

# Title and icon
pygame.display.set_caption("Shut It Down NAO")   # title
icon = pygame.image.load("icon/NAO Icon.png")   # icon
pygame.display.set_icon(icon)

# Background Image
lvl0ImgSrc = pygame.image.load("Images/Level 0.png")
imgSrcH = lvl0ImgSrc.get_height()
hRatio = scrH / imgSrcH
lvl0Img = pygame.transform.scale_by(lvl0ImgSrc, hRatio)

# Floor
floorH = 64

def background():
    screen.blit(lvl0Img, (0, 0))

# Player
playerImgSrc = pygame.image.load("Images/Bill Standing.png")
pImg = pygame.transform.scale_by(playerImgSrc, 4)
pW = pImg.get_width()
pH = pImg.get_height()
pX = 128   # player starting position
pY = scrH - floorH - pW   # player is on a floor
pV = 4

def player():
    global pX, pY
    screen.blit(pImg, (pX, pY))
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and pX > 0:
        pX -= pV
    if keys[pygame.K_d] and pX < scrW-pW:
        pX += pV

# Enemy
enemyImg = pygame.image.load("Images/NAO.png")

def enemy_activate():
    pass

# GAME LOOP
running = True
while running:
    screen.fill((0, 0, 0))   # default black background
    background()
    pygame.time.delay(10)   # time delay (in ms)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # quit condition
            running = False

    player()

    pygame.display.update()   # update game window