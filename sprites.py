import pygame
from main_functions import load_image, import_csv_layout, file_difficulty
import random
from Level import *
pygame.init()


player_sprite = pygame.sprite.Group()
mob_sprite = pygame.sprite.Group()
mobs_file = import_csv_layout('level/main_map1_Mobs.csv')
damage = pygame.mixer.Sound('layouts/hit3.mp3')
attack = pygame.mixer.Sound('layouts/attack.wav')


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
        if pygame.sprite.spritecollideany(self, danger_blocks) and self.event:
            self.lives -= 1
            damage.play()
            self.points -= NEGATIVE_FOR_BLOCK
            self.event = False
        if not pygame.sprite.spritecollideany(self, danger_blocks):
            self.event = True
        if pygame.sprite.spritecollideany(self, health):
            try:
                id_sprite = pygame.sprite.spritecollide(self, health, True)[0].id_image
                if id_sprite == BLUE_HEALTH[0]:
                    self.points += BLUE_HEALTH[1]
                elif id_sprite == ONE_HEARD[0]:
                    self.lives += ONE_HEARD[1]
                elif id_sprite == CHEST[0]:
                    self.points += CHEST[1]
                elif id_sprite == YELLOW_HEALTH[0]:
                    self.points += YELLOW_HEALTH[1]
                elif id_sprite == GREEN_HEALTH[0]:
                    self.points += GREEN_HEALTH[1]
                elif id_sprite == HALF_HEARD[0]:
                    self.lives += HALF_HEARD[1]

            except Exception as ex:
                print(ex)

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
        self.c = 3
        self.live = 3

    def minus(self, x, y):
        if self.rect.collidepoint(x, y):
            self.live -= 1
            if self.live < 1:
                self.kill()
                return 'kill'
            return 'live'

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.c % 3 == 0:
            if self.dir == 1:
                last_pos_x = self.pos_x
                last_rect_x = self.rect.x
                self.pos_x += self.go
                self.rect.x += self.go * TILESIZE
                if (not pygame.sprite.spritecollideany(self, floor)) or \
                        pygame.sprite.spritecollideany(self, danger_blocks):
                    self.pos_x = last_pos_x
                    self.rect.x = last_rect_x
                    self.go *= -1
            else:
                last_pos_y = self.pos_y
                last_rect_y = self.rect.y
                self.pos_y += self.go
                self.rect.y += self.go * TILESIZE
                if (not pygame.sprite.spritecollideany(self, floor)) or \
                        pygame.sprite.spritecollideany(self, danger_blocks):
                    self.pos_y = last_pos_y
                    self.rect.y = last_rect_y
                    self.go *= -1
            if pygame.sprite.spritecollideany(self, player_sprite):
                for i in player_sprite:
                    i.lives -= 1
                    damage.play()
                    i.points -= NEGATIVE_FOR_BLOCK
                    i.event = False
        self.c += 1


class AnimatedBossSprite(pygame.sprite.Sprite):
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
        self.live = 5
        self.c = 4

    def minus(self, x, y):
        if self.rect.collidepoint(x, y):
            self.live -= 1
            if self.live < 1:
                self.kill()
                return 'kill-b'
            return 'live'

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.dir = random.randint(1, 2)
        if self.c % 4 == 0:
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
            if pygame.sprite.spritecollideany(self, player_sprite):
                for i in player_sprite:
                    i.lives -= 1
                    damage.play()
                    i.points -= NEGATIVE_FOR_BLOCK
                    i.event = False
        self.c += 1