import pygame

from settings import *
from Level import Level, floor, wall, danger_blocks, health, all_sprites
from main_functions import load_image, import_csv_layout, file_difficulty
from Sound import Sound
from Header import Header

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


def pos_check(sprite):
    m = [(sprite.pos_x - 1, sprite.pos_y - 1), (sprite.pos_x - 1, sprite.pos_y), (sprite.pos_x - 1, sprite.pos_y + 1),
         (sprite.pos_x, sprite.pos_y + 1), (sprite.pos_x + 1, sprite.pos_y + 1), (sprite.pos_x + 1, sprite.pos_y),
         (sprite.pos_x + 1, sprite.pos_y - 1), (sprite.pos_x, sprite.pos_y - 1)]
    # for i in m:
    #     print('err')
        # if str(mobs_file[i[0]][i[1]][0]) == 'm':
        #     sprite.lives -= 1


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
        if (not pygame.sprite.spritecollideany(self, floor)) or pygame.sprite.spritecollideany(self, mob_sprite):
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
        pos_check(self)


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

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if pygame.sprite.spritecollideany(self, player_sprite):
            print(123)


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
        mob_sprite.draw(self.display)

        self.level.update()
        self.level.run()
        player_sprite.draw(self.display)
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.music.stop()
            if player.lives == 0:
                # pic = load_image('game_over.png', path='layouts')
                # self.display.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))
                # pygame.display.flip()
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
            header.draw(self.display)
            pygame.display.flip()
            self.clock.tick(15)

    def display_clear(self):
        self.display.fill('BLACK')


if __name__ == '__main__':
    game = Game()
    game.run()
