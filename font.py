import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED, WHITE
from functions import *

pygame.init()
# font_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Font:
    def __init__(self):
        self.spacing = 1
        self.char_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-,:+\'!?0123456789()/_=\\[]*\"<>;"
        font_img = pygame.image.load("Images/font/small_font.png")   # Credits to DaFluffyPotato
        current_char_width = 0
        self.characters = {}
        char_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:   # colour of the bar between each character
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.char_order[char_count]] = char_img.copy()   # append char_img as dict value
                char_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_height()
        self.height = self.characters["A"].get_height()
        self.space_img = pygame.Surface(self.characters["A"].get_size())

    def render(self, text, scale=1, colour=WHITE):
        x_offset = 0
        char_list = []
        for char in text:
            if char != " ":
                text_char_img = self.characters[char]
                char_list += [text_char_img]
                x_offset += text_char_img.get_width() + self.spacing
            else:
                char_list += [self.space_img]
                x_offset += self.space_width + self.spacing
        text_img = pygame.Surface((x_offset, self.height))
        x_offset = 0
        while len(char_list) > 0:
            char_img = char_list.pop(0)
            text_img.blit(char_img, (x_offset, 0))
            x_offset += char_img.get_width() + self.spacing
        text_img.set_colorkey(BLACK)
        text_img_copy = text_img.copy().convert_alpha()
        text_img_coloured = apply_colour(text_img_copy, colour)
        text_img_scaled = pygame.transform.scale_by(text_img_coloured, scale)
        return text_img_scaled

    """def demo(self):
        text1 = "This is my game font"
        text2 = "Credits to DaFluffyPotato! :)"
        self.running = True
        while self.running:
            font_screen.fill(BLACK)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
            text1_img = self.render(text1, 8)
            text2_img = self.render(text2, 2, RED)
            font_screen.blit(text1_img, (64, 64))
            font_screen.blit(text2_img, (64, 128))
            pygame.display.update()"""

game_font = Font()
# game_font.demo()
pygame.quit()