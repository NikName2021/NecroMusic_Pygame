from PIL import Image
from itertools import product
import os


img = Image.open('0x72_DungeonTilesetII_v1024.png')
img = img.convert('RGB')
w, h = img.size
d = 32
az = 0
grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
for i, j in grid:
    box = (j, i, j + d, i + d)
    # out = os.path.join('tiles', f'{az}.jpg')
    img.crop(box).save(f'tiles/{az}.jpg',)
    az += 1