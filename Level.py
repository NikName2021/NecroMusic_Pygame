import pygame
import pytmx
from main_functions import *
from settings import *


all_sprites = pygame.sprite.Group()
floor = pygame.sprite.Group()
wall = pygame.sprite.Group()
danger_blocks = pygame.sprite.Group()
health = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, image, pos_x, pos_y, id_image=0):
        super().__init__(tile_type, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILESIZE * pos_x, TILESIZE * pos_y)
        self.id_image = int(id_image)


class Level:
    def __init__(self, main_window):
        self.window = main_window
        self.layouts = self.create_map()
        self.images = self.load_all_image()

    def create_map(self):
        layouts = {
            'floor': (import_csv_layout('level/main_map1_Floor.csv'), floor),
            'wall': (import_csv_layout('level/main_map1_Walls.csv'), wall),
            'danger': (import_csv_layout('level/main_map1_Danger.csv'), danger_blocks),
            'health': (import_csv_layout('level/main_map1_Points_and_Health.csv'), health)
        }
        return layouts

    def load_all_image(self):
        images = {}
        for i in range(0, 1024):
            images[i] = load_image(f'{i}.png', (0, 0, 0))
        return images

    def update(self):
        for i, j in self.layouts.items():
            for n, g in enumerate(j[0]):
                for q, m in enumerate(g):
                    if m != '-1':
                        image = self.images[int(m)]
                        Tile(j[1], image,  q, n, m)

    def run(self):
        floor.draw(self.window)
        wall.draw(self.window)
        danger_blocks.draw(self.window)
        health.draw(self.window)
