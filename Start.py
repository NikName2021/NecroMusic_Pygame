import pygame
import pygame_menu

from main import Game
from settings import *
from connection import con, cur

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))


def start_the_game():
    game = Game()
    game.display_clear()
    game.killer()
    code_play = game.run()


def set_difficulty(value, difficulty):
    with open('setting.txt', 'w', encoding='UTF-8') as file:
        file.write(str(difficulty))


def file_difficulty():
    with open('setting.txt', 'r', encoding='UTF-8') as file:
        dif = int(file.readline())
    return difficults[dif]


def record():
    main = cur.execute("SELECT MAX(result) FROM games;").fetchone()
    if main:
        return main[0]
    else:
        return 0


menu = pygame_menu.Menu('Crazy Dungeons', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Играть', start_the_game)
menu.add.button('Выйти', pygame_menu.events.EXIT)
menu.add.selector('Сложность :',
                  [(key, name) for name, key in difficults.items()], onchange=set_difficulty).set_value(file_difficulty())
menu.add.label(f'Рекорд: {record()}')

if __name__ == '__main__':
    menu.mainloop(surface)
