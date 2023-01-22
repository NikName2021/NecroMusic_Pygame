import pygame
import random

from settings import *
from Level import Level, floor, wall, danger_blocks, health, all_sprites
from main_functions import load_image, import_csv_layout, file_difficulty
from Sound import Sound
from Header import Header
from connection import con, cur
from sprites import *


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
        header = Header(player, self.display)
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
                elif player.pos_x != i and player.pos_y != j and mobs_file[i][j] == 'm22':
                    mob = AnimatedBossSprite(503, 510, mob_sprite)
                    mob.rect = mob.image.get_rect()
                    mob.pos_x = j
                    mob.pos_y = i
                    mob.rect.x = j * TILESIZE
                    mob.rect.y = i * TILESIZE
                    mob_sprite.add(mob)
                    all_sprites.add(mob)

        mob_sprite.draw(self.display)

        count = False
        reset = True
        self.level.update()
        self.level.run()
        player_sprite.draw(self.display)
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.music.stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i in mob_sprite:
                        if i.minus(x, y) == 'kill':
                            player.points += NEGATIVE_FOR_BLOCK
                            attack.play()
                        elif i.minus(x, y) == 'live':
                            attack.play()
                        elif i.minus(x, y) == 'kill-b':
                            player.points += 3 * NEGATIVE_FOR_BLOCK
                            attack.play()

            if len(mob_sprite.sprites()) == 0:
                if reset:
                    self.display_clear()
                    self.save_result(player)
                pic = load_image('winner.jpg', path='layouts')
                self.display.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))
                pygame.display.flip()
                self.music.stop()
                reset = False

            if player.lives == 0:
                if reset:
                    self.display_clear()
                    self.save_result(player)
                pic = load_image('game_over.png', path='layouts')
                self.display.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))
                pygame.display.flip()
                self.music.stop()
                reset = False
            else:
                player_sprite.update()
                mob_sprite.update()
                self.display.fill((0, 0, 0))
                self.level.run()
                player_sprite.draw(self.display)
                mob_sprite.draw(self.display)
                header.draw(self.display)
                pygame.display.flip()
                self.clock.tick(15)

    def display_clear(self):
        self.display.fill((0, 0, 0))
        pygame.display.flip()

    def killer(self):
        for i in all_sprites:
            i.kill()
        for i in player_sprite:
            i.kill()

    def save_result(self, player):
        cur.execute("INSERT INTO games(result) VALUES(?)", (player.points,))
        con.commit()


if __name__ == '__main__':
    game = Game()
    game.run()
