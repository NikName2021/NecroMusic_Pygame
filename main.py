import pygame

from settings import *
from Level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.display)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.level.update()
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()