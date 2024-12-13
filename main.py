import pygame
pygame.init()   # initialise pygame

scrWidth = 1000
scrHeight = 600
screen = pygame.display.set_mode([scrWidth, scrHeight])   # create game screen [W,H]

# Title and icon
pygame.display.set_caption("Shut It Down NAO")   # title
icon = pygame.image.load("icon/NAO Icon.png")   # icon
pygame.display.set_icon(icon)

# Floor
floorHeight = 120

# Player
playerImg = pygame.image.load("Images/Bill Standing.png")
playerX = scrWidth / 2   # player is at the center
playerY = scrHeight - floorHeight   # player is on a floor
playerV = 1

def player():
    screen.blit(playerImg, (playerX, playerY))

# GAME LOOP
running = True
while running:
    screen.fill((0, 0, 0))   # default black background
    pygame.time.delay(10)   # time delay (in ms)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # quit condition
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerX -= playerV
    if keys[pygame.K_d]:
        playerX += playerV
    player()
    pygame.display.update()   # update game window