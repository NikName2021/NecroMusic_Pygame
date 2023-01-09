import pygame

from settings import *
from Level import Level, floor, wall, all_sprites
from main_functions import load_image


player_sprite = pygame.sprite.Group()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, startpos, endpos, sprite_group):
        super().__init__(sprite_group)
        self.frames = []
        for i in range(startpos, endpos + 1):
            self.frames.append(load_image(f'{i}.jpg'))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.pos_x = 0
        self.pos_y = 0

    def handle_keys(self):
        key = pygame.key.get_pressed()
        last_pos_x = self.pos_x
        last_pos_y = self.pos_y
        last_rect_x = self.rect.x
        last_rect_y = self.rect.y
        if key[pygame.K_DOWN]:
            self.pos_y += 1
            self.rect.y += TILESIZE
        elif key[pygame.K_UP]:
            self.pos_y -= 1
            self.rect.y -= TILESIZE
        if key[pygame.K_RIGHT]:
            self.pos_x += 1
            self.rect.x += TILESIZE
        elif key[pygame.K_LEFT]:
            self.pos_x -= 1
            self.rect.x -= TILESIZE
        if not pygame.sprite.spritecollideany(self, floor):
            self.pos_x = last_pos_x
            self.pos_y = last_pos_y
            self.rect.x = last_rect_x
            self.rect.y = last_rect_y

    def update(self):
        self.handle_keys()
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.display)

    def run(self):
        camera = Camera()
        player = AnimatedSprite(40, 47, player_sprite)
        player.rect = player.image.get_rect()
        player_sprite.add(player)
        pos_x = WIDTH // TILESIZE
        pos_y = HEIGHT // TILESIZE
        current_check = []
        for i in self.level.layouts['floor'][0]:
            current_check.append(i[0:pos_x])
        current_check = current_check[0:pos_y]
        player.pos_x = pos_x // 2 + 1
        player.pos_y = pos_y // 2 + 1
        if current_check[player.pos_y][player.pos_x] == '-1':
            cx = player.pos_x
            cy = player.pos_y
            r = 1000000000
            tx = player.pos_x
            ty = player.pos_y
            fl = False
            while tx >= 0:
                if current_check[ty][tx] != '-1':
                    fl = True
                    break
                tx -= 1
            if fl and (player.pos_x - tx) < r:
                r = player.pos_x - tx
                cx = tx
                cy = ty
            tx = player.pos_x
            ty = player.pos_y
            fl = False
            while tx < WIDTH // TILESIZE:
                if current_check[ty][tx] != '-1':
                    fl = True
                    break
                tx += 1
            if fl and (tx - player.pos_x) < r:
                r = tx - player.pos_x
                cx = tx
                cy = ty
            tx = player.pos_x
            ty = player.pos_y
            fl = False
            while ty >= 0:
                if current_check[ty][tx] != '-1':
                    fl = True
                    break
                ty -= 1
            if fl and (player.pos_y - ty) < r:
                r = player.pos_y - ty
                cx = tx
                cy = ty
            tx = player.pos_x
            ty = player.pos_y
            fl = False
            while ty < HEIGHT // TILESIZE:
                if current_check[ty][tx] != '-1':
                    fl = True
                    break
                ty += 1
            if fl and (ty - player.pos_y) < r:
                r = ty - player.pos_y
                cx = tx
                cy = ty
            player.pos_x = cx
            player.pos_y = cy
        player.rect.x = player.pos_x * TILESIZE
        player.rect.y = player.pos_y * TILESIZE
        running = True
        self.level.update()
        self.level.run()
        player_sprite.draw(self.display)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            player_sprite.update()
            self.display.fill((0, 0, 0))
            self.level.run()
            player_sprite.draw(self.display)
            for sprite in all_sprites:
                camera.apply(sprite)
            for sprite in floor:
                camera.apply(sprite)
            for sprite in wall:
                camera.apply(sprite)
            pygame.display.flip()
            camera.update(player)
            self.clock.tick(15)


if __name__ == '__main__':
    game = Game()
    game.run()
