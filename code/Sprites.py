import pygame
from settings import *
from SQL_login import *
from SQL_register import *
import math
import random
import time

score = 0

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x , y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(WHITE)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self.score = 0
        self._layer = Player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.font = pygame.font.Font('../font/Retro.ttf', 30)
        self.score_text = 0

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.cool_down_count = 0

        self.image = self.game.character_spritesheet.get_sprite(54, 66, pixel_L, pixel_H)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        for enemy in hits:
            self.score += 1

    def update_score(self):
        global Pass
        if Pass:
            # Update score in database
            c.execute("UPDATE users SET score = ? WHERE username = ?", (self.score, self.username))
            conn.commit()

        # Render score text
        self.score_text = self.game.font.render(f"Score: {self.score}", True, WHITE)

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        self.score += len(hits)

    def cooldown(self):
        if self.cool_down_count >= 40:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def movement(self):
        self.cooldown()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and self.cool_down_count == 0):
            for sprite in self.game.all_sprites:
                sprite.rect.x += Player_speed
            self.x_change -= Player_speed
            self.facing = 'left'
            self.cool_down_count = 1
        if (keys[pygame.K_RIGHT] and self.cool_down_count == 0):
            for sprite in self.game.all_sprites:
                sprite.rect.x -= Player_speed
            self.x_change += Player_speed
            self.facing = 'right'
            self.cool_down_count = 1
        if (keys[pygame.K_UP] and self.cool_down_count == 0):
            for sprite in self.game.all_sprites:
                sprite.rect.y += Player_speed
            self.y_change -= Player_speed
            self.facing = 'up'
            self.cool_down_count = 1
        if (keys[pygame.K_DOWN] and self.cool_down_count == 0):
            for sprite in self.game.all_sprites:
                sprite.rect.y -= Player_speed
            self.y_change += Player_speed
            self.facing = 'down'
            self.cool_down_count = 1

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += Player_speed
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= Player_speed

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += Player_speed
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= Player_speed

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(54, 492, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(198, 492, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(342, 492, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(486, 492, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(630, 492, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(774, 492, pixel_L, pixel_H)]

        up_animations = [self.game.character_spritesheet.get_sprite(54, 783, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(198, 783, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(342, 783, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(486, 783, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(630, 783, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(774, 783, pixel_L, pixel_H)]

        left_animations = [self.game.character_spritesheet.get_sprite(50, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(195, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(338, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(482, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(626, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(770, 204, pixel_L, pixel_H)]

        right_animations = [self.game.character_spritesheet.get_sprite(50, 636, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(195, 636, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(338, 6362, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(482, 636, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(626, 636, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(770, 636, pixel_L, pixel_H)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(54, 66, pixel_L, pixel_H)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(54, 354, pixel_L, pixel_H)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(195, 204, pixel_L, pixel_H)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(195, 636, pixel_L, pixel_H)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 6:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = Enemy_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(32, 47)

        self.image = self.game.enemy_spritesheet.get_sprite(32, 12, 63, 51)
        self.image.set_colorkey(WHITE)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= Enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += Enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        right_animations = [self.game.enemy_spritesheet.get_sprite(32, 12, 63, 51),
                           self.game.enemy_spritesheet.get_sprite(152, 12, 71, 51),
                           self.game.enemy_spritesheet.get_sprite(272, 12, 87, 51),
                           self.game.enemy_spritesheet.get_sprite(416, 12, 63, 51),
                           self.game.enemy_spritesheet.get_sprite(548, 4, 55, 51)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(32, 396, 63, 51),
                           self.game.enemy_spritesheet.get_sprite(157, 396, 71, 51),
                           self.game.enemy_spritesheet.get_sprite(280, 396, 87, 51),
                           self.game.enemy_spritesheet.get_sprite(414, 396, 63, 51),
                           self.game.enemy_spritesheet.get_sprite(546, 388, 55, 51)]

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(32, 396, 63, 51)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(32, 12, 63, 51)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = Block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.block_sprite.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = Ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('../font/Retro.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = Score_layer
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = tilesize
        self.width = tilesize

        self.animation_loop = 0

        self.image = self.game.character_spritesheet.get_sprite(54, 66, pixel_L, pixel_H)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        for enemy in hits:
            self.game.player.score += 1

    def animate(self):
        direction = self.game.player.facing

        down_animations = [self.game.character_spritesheet.get_sprite(45, 930, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(195, 930, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(342, 930, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(487, 930, pixel_L, pixel_H)]

        up_animations = [self.game.character_spritesheet.get_sprite(55, 1218, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(177, 1218, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(324, 1218, pixel_L, pixel_H),
                         self.game.character_spritesheet.get_sprite(486, 1218, pixel_L, pixel_H)]

        left_animations = [self.game.character_spritesheet.get_sprite(48, 1361, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(152, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(340, 204, pixel_L, pixel_H),
                           self.game.character_spritesheet.get_sprite(483, 204, pixel_L, pixel_H)]

        right_animations = [self.game.character_spritesheet.get_sprite(55, 1074, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(168, 1074, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(321, 1074, pixel_L, pixel_H),
                            self.game.character_spritesheet.get_sprite(482, 1074, pixel_L, pixel_H)]

        if direction =='up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()

        if direction =='down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()

        if direction =='left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 4:
                self.kill()