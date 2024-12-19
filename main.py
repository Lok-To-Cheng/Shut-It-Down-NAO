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
        # Sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.backgrounds = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

    def new(self, lvl_no):
        self.playing = True   # Player is playing
        # Background, Enemies, Player
        self.background = Background(self, lvl_no)
        if lvl_no==0:
            pass
        else:
            pass
        self.player = Player(self, lvl_no)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def scroll(self, speed):
        if speed < 0:   # scroll to the left
            if (self.background.rect.x < 0):
                if (self.player.x < SCROLL_THRESHOLD):
                    for sprite in self.all_sprites:
                        sprite.rect.x -= speed
                    return True
                return False
            return False
        else:    # scroll to the right
            if (self.background.rect.x > SCREEN_WIDTH - self.background.rect.width):
                if (self.player.x > SCROLL_THRESHOLD):
                    for sprite in self.all_sprites:
                        sprite.rect.x -= speed
                    return True
                return False
            return False

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
        self.background = Background(self)
        title_row1 = self.font.render("Shut It Down", 8)
        title_row2 = self.font.render("NAO", 16, RED)
        hint = self.font.render("CLICK YELLOW DOOR TO START", 4, YELLOW)
        door_button = Button(768, 496, 64, 80, YELLOW)
        while intro:
            self.screen.fill(BLACK)
            self.screen.blit(self.background.image, (0, 0))
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
game.new(1)
while game.running:
    game.start()
    game.over()

pygame.quit()
sys.exit()





















