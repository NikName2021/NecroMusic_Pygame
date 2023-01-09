from csv import reader
import pygame, os, sys


def import_csv_layout(path):
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        return [list(row) for row in layout]


def load_image(name, colorkey=-1):
    fullname = os.path.join('tiles', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == -1:
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    elif colorkey is not None:
        image = image.convert()
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    pygame.image.save(image, "out_test/image.jpg")
    return image
