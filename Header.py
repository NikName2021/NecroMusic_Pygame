import pygame
from settings import *
from main_functions import *


class Header:
    def __init__(self, player, display):
        pygame.init()
        self.player = player
        self.display = display
        self.heart = load_image('530.png')
        self.coin = load_image('629.png')

    def draw(self, display):
        font = pygame.font.Font(None, 50)
        text1 = font.render(str(self.player.lives), True, (255, 255, 255))
        text1_w = text1.get_width()
        text1_h = text1.get_height()
        display.blit(self.heart, (0, 0))
        display.blit(text1, (32, 0))
        text2 = font.render(str(self.player.points), True, (255, 255, 255))
        display.blit(self.coin, (32 + text1_w, 0))
        display.blit(text2, (64 + text1_w, 0))