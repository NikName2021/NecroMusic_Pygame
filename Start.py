import pygame
import pygame_menu
from main import Game
from settings import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))


def start_the_game():
    game = Game()
    var = pygame_menu.events.EXIT
    game.run()


menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

name = menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
