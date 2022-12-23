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
        self.level.update()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.level.run()
            pygame.display.update()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()