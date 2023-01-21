import pygame
import pytmx
from main_functions import *
from settings import *


all_sprites = pygame.sprite.Group()
floor = pygame.sprite.Group()
wall = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, image, pos_x, pos_y):
        super().__init__(tile_type, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILESIZE * pos_x, TILESIZE * pos_y)


class Sound:
    def __init__(self):
        pygame.mixer.music.load('laouts/necrotic_music.mp3')
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()


class Level:
    def __init__(self, main_window):
        self.window = main_window
        self.layouts = self.create_map()
        self.images = self.load_all_image()

        music = Sound()

    def create_map(self):
        layouts = {
            'floor': (import_csv_layout('level/main_map1_Floor.csv'), floor),
            'wall': (import_csv_layout('level/main_map1_Walls.csv'), wall)
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
                        Tile(j[1], image,  q, n)

    def run(self):
        floor.draw(self.window)
        wall.draw(self.window)


    # def update(self):
    #     for layer in self.gameMap.visible_layers:
    #         if isinstance(layer, pytmx.TiledTileLayer):
    #             for x, y, gid, in layer:
    #                 tile = self.gameMap.get_tile_image_by_gid(gid)
    #                 if tile:
    #                     self.window.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))