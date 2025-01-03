# MODULES
import pygame
import sys
import random

from pygame import K_KP_ENTER

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
        self.icon = pygame.image.load("Images/Icon.png")  # icon
        pygame.display.set_icon(self.icon)
        # Frame delay
        self.frame_delay = 0
        # Game starts at Level 0
        self.level = 0
        # All sprites group
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.backgrounds = pygame.sprite.LayeredUpdates()
        # Game states
        self.running = True
        self.on_title = False
        self.on_intro = False
        self.playing = False
        self.lose = False
        self.win = False

    def new(self):
        # Initialise new sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.backgrounds = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.playing = True   # Player is playing
        # Background, Enemies, Player
        self.background = Background(self, self.level)
        if self.level==0:
            for i in range(5):
                self.enemy = Enemy(self)
        else:
            for i in range(20):
                self.enemy = Enemy(self)
        self.player = Player(self)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw_status(self):
        self.lvl_status = f"LEVEL {self.level}"
        self.player_hp = f"HP: {self.player.hp}"
        self.staple_count = f"[: {self.player.staples_remaining}x"
        lvl_status = self.font.render(self.lvl_status, 4, PURPLE)
        player_hp = self.font.render(self.player_hp, 4, PURPLE)
        staple_count = self.font.render(self.staple_count, 4, PURPLE)
        self.screen.blit(lvl_status, (16, 16))
        self.screen.blit(player_hp, (16, 48))
        self.screen.blit(staple_count, (16, 84))

    def draw_instructions(self):
        self.controls_direction = "A: LEFT   D: RIGHT"
        self.controls_shoot = "SPACE: SHOOT"
        controls_direction = self.font.render(self.controls_direction, 2, WHITE)
        controls_shoot = self.font.render(self.controls_shoot, 2, WHITE)
        self.screen.blit(controls_direction, (256, 240))
        self.screen.blit(controls_shoot, (256, 264))

    def scroll(self, player_speed):
        if player_speed < 0:   # scroll to the left
            if (self.background.rect.x < 0):
                if (self.player.x < SCROLL_THRESHOLD):
                    for sprite in self.all_sprites:
                        sprite.rect.x -= player_speed
                    return True
                return False
            return False
        else:    # scroll to the right
            if (self.background.rect.x > SCREEN_WIDTH - self.background.rect.width):
                if (self.player.x > SCROLL_THRESHOLD):
                    for sprite in self.all_sprites:
                        sprite.rect.x -= player_speed
                    return True
                return False
            return False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_status()
        if self.level==0: self.draw_instructions()
        self.clock.tick(FPS)
        pygame.display.update()

    def title_screen(self):
        self.on_title = True
        self.background = Background(self)
        title_row1 = self.font.render("Shut It Down", 8)
        title_row2 = self.font.render("NAO", 16, RED)
        author = self.font.render("made by Jasper Cheng", 4, GREY)
        hint = self.font.render("CLICK YELLOW DOOR TO START", 4, YELLOW)
        door_button = Button(800, 536, 64, 80, YELLOW)
        while self.on_title:
            self.screen.fill(BLACK)
            self.screen.blit(self.background.image, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            # Draw screen
            self.screen.blit(title_row1, (32, 32))
            self.screen.blit(title_row2, (32, 108))
            self.screen.blit(author, (32, 216))
            self.screen.blit(hint, (32, 512))
            self.screen.blit(door_button.image, door_button.rect)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.on_title = False
                    self.running = False
            if door_button.is_pressed(mouse_pos, mouse_pressed):
                self.on_title = False
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        cont = "Press K to continue"
        play = "Press K to play"
        cont_rendered = self.font.render(cont, 4, WHITE)
        play_rendered = self.font.render(play, 4, YELLOW)
        weapon = pygame.image.load("Images/CIRCUIT JAMMER 3000.png")
        weapon = pygame.transform.scale_by(weapon, 32)
        weapon_rect = weapon.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 128))
        expressions = Expressions()
        intro_text = ["I can't believe this is happening...",
                      "This is my worst open day exhibition ever!",
                      "I spent 3 months programming my NAO robots...",
                      "and now they're are attacking everyone!",
                      "sigh.",
                      "Now I have no choice but to stop them with my",
                      "CIRCUIT JAMMER 3000!!!!!",
                      "It's a very powerful stapler.",
                      "Ready or not, here I come!"]
        intro_text_rendered = list(map(lambda text: self.font.render(text, 4, WHITE), intro_text))
        self.on_intro = True
        i = 0
        self.frame_delay = 0
        while self.on_intro:
            self.screen.fill(BLACK)
            self.screen.blit(expressions.sprites[i], (32, 32))
            self.screen.blit(intro_text_rendered[i], (192, 32))
            if i==6 or i==7:
                self.screen.blit(weapon, weapon_rect)
            if i < len(intro_text) - 1:
                self.screen.blit(cont_rendered, (720, 512))
            else:
                self.screen.blit(play_rendered, (720, 512))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.on_intro = False
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                if self.frame_delay == FRAME_PER_EVENT:
                    # next intro line
                    if i < len(intro_text) - 1: i += 1
                    else: self.on_intro = False
            self.frame_delay = (self.frame_delay % FRAME_PER_EVENT) + 1
            self.clock.tick(FPS)
            pygame.display.update()

    def start(self):   # gameplay loop
        self.frame_delay = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.player not in self.all_sprites:
                self.playing = False
                self.lose = True
            elif (len(self.enemies) == 0):
                self.playing = False
                self.win = True
            else: self.frame_delay = (self.frame_delay % FRAME_PER_EVENT) + 1

    def over(self):
        if self.lose:
            self.level_fail()
        if self.win:
            self.level_clear()

    def level_fail(self):
        game_over = self.font.render("GAME OVER!", 16, RED)
        try_again_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - FLOOR[0] - 48, 336, 96, BLACK, "TRY AGAIN", RED, 8, RED, 8)
        while self.lose:
            self.screen.fill(BLACK)
            game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over, game_over_rect)
            self.screen.blit(try_again_button.image, try_again_button.rect)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.lose = False
                    self.running = False
            if try_again_button.is_pressed(mouse_pos, mouse_pressed):
                self.lose = False
            pygame.display.update()

    def level_clear(self):
        you_win = self.font.render("YOU WIN!", 16, BLACK)
        you_win_rect = you_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        next_lvl_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - FLOOR[0] - 48, 336, 96, WHITE, "NEXT LEVEL", BLACK, 8, BLACK, 8)
        congrats = self.font.render("CONGRATULATIONS!", 8, BLACK)
        congrats_rect = congrats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 96))
        while self.win:
            self.screen.fill(WHITE)
            self.screen.blit(you_win, you_win_rect)
            if self.level < NUM_LEVELS - 1:
                self.screen.blit(next_lvl_button.image, next_lvl_button.rect)
            else:
                self.screen.blit(congrats, congrats_rect)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.win = False
                    self.running = False
            if next_lvl_button.is_pressed(mouse_pos, mouse_pressed):
                self.win = False
                self.level += 1
            pygame.display.update()

game = Game()
game.title_screen()
game.intro_screen()
while game.running:
    game.new()
    game.start()
    game.over()

pygame.quit()
sys.exit()





















