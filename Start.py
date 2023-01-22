import pygame
import pygame_menu

from main import Game
from settings import *
from connection import con, cur

pygame.init()
with open('volume.txt', 'w', encoding='UTF-8') as file:
    file.write('50')
surface = pygame.display.set_mode((WIDTH, HEIGHT))


def start_the_game():
    game = Game()
    game.display_clear()
    game.killer()
    game.run()


def file():
    with open('setting.txt', 'r', encoding='UTF-8') as file:
        dif = [int(line.rstrip()) for line in file]

    return dif


def set_difficulty(value, difficulty):
    with open('setting.txt', 'w', encoding='UTF-8') as file:
        file.write(str(difficulty))


def set_volume(value, volume):
    with open('volume.txt', 'w', encoding='UTF-8') as file:
        file.write(str(volume))


def set_map(value, difficulty):
    with open('setting.txt', 'w', encoding='UTF-8') as file:
        file.write(str(difficulty))


def file_difficulty():
    return difficults[file()[0]]


def map_value():
    return MAPS[file()[1]]


def record():
    main = cur.execute("SELECT MAX(result) FROM games;").fetchone()
    if main and not main[0] is None:
        return main[0]
    else:
        return 0


menu = pygame_menu.Menu('Crazy Dungeons', 500, 400,
                        theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Играть', start_the_game)
menu.add.button('Выйти', pygame_menu.events.EXIT)
menu.add.selector('Сложность :',
                  [(key, name) for name, key in difficults.items()], onchange=set_difficulty).set_value(file_difficulty())
menu.add.selector('Громкость музыки :',
                  [('Нет', 0), ('10%', 10), ('20%', 20), ('30%', 30), ('40%', 40), ('50%', 50), ('60%', 60),
                   ('70%', 70), ('80%', 80), ('90%', 90), ('100%', 100)], onchange=set_volume).set_value(5)

# menu.add.selector('Уровень :',
#                   [(key, name) for name, key in MAPS.items()], onchange=set_map).set_value(map_value())

menu.add.label(f'Рекорд: {record()}')

if __name__ == '__main__':
    menu.mainloop(surface)
