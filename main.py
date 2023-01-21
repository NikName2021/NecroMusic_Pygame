import pygame
import random

from settings import *
from Level import Level, floor, wall, danger_blocks, all_sprites
from main_functions import load_image, import_csv_layout, file_difficulty
from Sound import Sound

pygame.init()

player_sprite = pygame.sprite.Group()
mob_sprite = pygame.sprite.Group()
mobs_file = import_csv_layout('level/main_map1_Mobs.csv')
damage = pygame.mixer.Sound('layouts/hit3.mp3')


def repos(lx, nx, ly, ny):
    dx = nx - lx
    dy = ny - ly
    for sprite in all_sprites:
        sprite.rect.x -= dx
        sprite.rect.y -= dy


class PlayerMovableSprite(pygame.sprite.Sprite):
    def __init__(self, startpos, endpos, sprite_group):
        super().__init__(sprite_group)
        self.frames = []
        for i in range(startpos, endpos + 1):
            self.frames.append(load_image(f'{i}.png'))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.pos_x = 0
        self.pos_y = 0
        self.lives = file_difficulty()
        self.money = 0
        self.event = True
        self.points = 0

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
        if pygame.sprite.spritecollideany(self, mob_sprite):
            self.lives -= 1
            damage.play()
            self.points -= NEGATIVE_FOR_BLOCK
            self.event = False
        if pygame.sprite.spritecollideany(self, danger_blocks) and self.event:
            self.lives -= 1
            damage.play()
            self.points -= NEGATIVE_FOR_BLOCK
            self.event = False
        if not pygame.sprite.spritecollideany(self, danger_blocks):
            self.event = True

        repos(last_rect_x, self.rect.x, last_rect_y, self.rect.y)
        self.rect.x = last_rect_x
        self.rect.y = last_rect_y

    def update(self):
        self.handle_keys()
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class AnimatedMobSprite(pygame.sprite.Sprite):
    def __init__(self, startpos, endpos, sprite_group):
        super().__init__(sprite_group)
        self.frames = []
        for i in range(startpos, endpos + 1):
            self.frames.append(load_image(f'{i}.png'))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.pos_x = 0
        self.pos_y = 0
        self.go = 1
        self.dir = random.randint(1, 2)
        self.move = 1
        self.live = 3

    def minus(self, x, y):
        if self.rect.collidepoint(x, y):
            self.live -= 1
            if self.live < 1:
                self.kill()
                return True
            return False

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.move == 1:
            if self.dir == 1:
                last_pos_x = self.pos_x
                last_rect_x = self.rect.x
                self.pos_x += self.go
                self.rect.x += self.go * TILESIZE
                if (not pygame.sprite.spritecollideany(self, floor)) or pygame.sprite.spritecollideany(self,
                                                                                                       danger_blocks):
                    self.pos_x = last_pos_x
                    self.rect.x = last_rect_x
                    self.go *= -1
            else:
                last_pos_y = self.pos_y
                last_rect_y = self.rect.y
                self.pos_y += self.go
                self.rect.y += self.go * TILESIZE
                if (not pygame.sprite.spritecollideany(self, floor)) or pygame.sprite.spritecollideany(self,
                                                                                                       danger_blocks):
                    self.pos_y = last_pos_y
                    self.rect.y = last_rect_y
                    self.go *= -1
        self.move *= -1


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.display)
        self.music = Sound()

    def run(self):
        player = PlayerMovableSprite(40, 47, player_sprite)
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
        mobs_dict = dict(m1=(168, 176), m2=(296, 304), m3=(488, 496), m4=(695, 702), m5=(251, 254), m6=(627, 629),
                         m7=(183, 190), m8=(530, 532))
        
        for i in range(len(mobs_file)):
            for j in range(len(mobs_file[i])):
                if player.pos_x != i and player.pos_y != j and mobs_file[i][j] in mobs_dict.keys():
                    mob = AnimatedMobSprite(mobs_dict[mobs_file[i][j]][0], mobs_dict[mobs_file[i][j]][1], mob_sprite)
                    mob.rect = mob.image.get_rect()
                    mob.pos_x = j
                    mob.pos_y = i
                    mob.rect.x = j * TILESIZE
                    mob.rect.y = i * TILESIZE
                    mob_sprite.add(mob)
                    all_sprites.add(mob)
        mob_sprite.draw(self.display)
        
        running = True
        count = False
        self.level.update()
        self.level.run()
        player_sprite.draw(self.display)
        pygame.display.flip()
        heart = load_image('530.png')
        coin = load_image('629.png')
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.music.stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i in mob_sprite:
                        if i.minus(x, y):
                            player.points += NEGATIVE_FOR_BLOCK

            if len(mob_sprite.sprites()) == 0:
                for i in all_sprites:
                    i.kill()
                self.display.fill((0, 0, 0))
                pygame.display.flip()
                self.music.stop()
                return 1

            if player.lives == 0:
                for i in all_sprites:
                    i.kill()
                self.display.fill((0, 0, 0))
                pygame.display.flip()
                self.music.stop()
                return 1 

            player_sprite.update()
            mob_sprite.update()
            self.display.fill((0, 0, 0))
            self.level.run()
            player_sprite.draw(self.display)
            mob_sprite.draw(self.display)

            font = pygame.font.Font(None, 50)
            text1 = font.render(str(player.lives), True, (255, 255, 255))
            text1_w = text1.get_width()
            text1_h = text1.get_height()
            self.display.blit(heart, (0, 0))
            self.display.blit(text1, (32, 0))
            text2 = font.render(str(player.money), True, (255, 255, 255))
            self.display.blit(coin, (32+text1_w, 0))
            self.display.blit(text2, (64+text1_w, 0))

            points = font.render(str(player.points), True, (255, 255, 255))
            self.display.blit(points, (WIDTH - 64, 5))

            pygame.display.flip()
            self.clock.tick(15)
            
    def display_clear(self):
        self.display.fill('BLACK')


if __name__ == '__main__':
    game = Game()
    game.run()
