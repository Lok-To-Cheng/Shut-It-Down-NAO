import pygame
import random

pygame.init()   # initialise pygame

# Display setup
scrW, scrH = 800, 600
screen = pygame.display.set_mode((scrW, scrH))
pygame.display.set_caption("Simple Class-based Game Example with Collision Detection")

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 375   # initial position
        self.rect.y = 240

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, scrW-150)
        self.rect.y = random.randint(0, scrH-150)

# Sprite groups (PyCharm, DO YOUR THING!!)
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Add sprite classes into groups
player = Player()
all_sprites.add(player)

for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# MAIN GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Collision detection
    if pygame.sprite.spritecollideany(player, enemies):
        print("Collision detected.")

    # Clear screen
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()