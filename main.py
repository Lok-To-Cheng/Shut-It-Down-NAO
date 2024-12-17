# MODULES
import pygame
import sys
import random

# PYTHON FILES
from config import *
from sprites import *
from font import game_font
from functions import *

# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = game_font
        # Title and icon
        self.title = "Shut It Down NAO!"  # title
        pygame.display.set_caption(self.title)
        self.icon = pygame.image.load("icon/NAO Icon.png")  # icon
        pygame.display.set_icon(self.icon)
        # Title screen background
        title_background_img = pygame.image.load("Images/MCS.png")
        self.title_background = pygame.transform.scale(title_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Level backgrounds

    def new(self, lvl_no):
        self.playing = True   # Player is playing
        # Sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.level_backgrounds = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        # Player
        self.player = Player(self, lvl_no)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        keys_down = pygame.key.get_pressed()
        player.move(keys_down)  # user input into player movement
        if keys_down[pygame.K_SPACE]:
            staple = player.shoot()
            movingSprites.add(staple)
            bullets.add(staple)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def start(self):   # gameplay loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def over(self):
        pass

    def title_screen(self):
        intro = True
        title_row1 = self.font.render("Shut It Down", 8)
        title_row2 = self.font.render("NAO", 16, RED)
        hint = self.font.render("CLICK YELLOW DOOR TO START", 4, YELLOW)
        door_button = Button(768, 496, 64, 80, YELLOW)
        while intro:
            self.screen.fill(BLACK)
            self.screen.blit(self.title_background, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            # Draw screen
            self.screen.blit(title_row1, (32, 32))
            self.screen.blit(title_row2, (32, 128))
            self.screen.blit(hint, (32, 512))
            self.screen.blit(door_button.image, door_button.rect)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    intro = False
                    self.running = False
            if door_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            self.clock.tick(FPS)
            pygame.display.update()

game = Game()
game.title_screen()
game.new(0)
while game.running:
    game.start()
    game.over()

pygame.quit()
sys.exit()





















