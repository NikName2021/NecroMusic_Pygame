import pygame
import pytmx


class Level():
    def __init__(self, main_window):
        pygame.init()
        self.gameMap = pytmx.load_pygame("main_map.tmx")
        self.window = main_window

    def update(self):
        for layer in self.gameMap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if tile:
                        self.window.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))