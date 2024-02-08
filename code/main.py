import pygame
from Sprites import *
from settings import *
from pygame import mixer
from SQL_login import *
from SQL_register import *
import sys
import sqlite3

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('../font/Retro.ttf', 64)

        self.hit_enemies = set()

        self.character_spritesheet = Spritesheet('../character/player_bb.png')
        self.terrain_spritesheet = Spritesheet('../Sprites/Grass_64x64.png')
        self.block_sprite = Spritesheet('../Sprites/rock.png')
        self.enemy_spritesheet = Spritesheet('../Sprites/slime_all.png')
        self.intro_background = pygame.image.load('../Sprites/sky_crop.png')
        self.menu_background = pygame.image.load('../Sprites/birb.png')
        self.go_background = pygame.image.load('../Sprites/sky_night.png')
        self.background_music = mixer.music.load('../music/Journey.mp3')

    def createTilemap(self, input_boxes):
        for row_index, row in enumerate(World_map):
            for col_index, col in enumerate(row):
                Ground(self, col_index, row_index)
                if col == 'X':
                    Block(self, col_index, row_index)
                if col == 'E':
                    Enemy(self, col_index, row_index)
                if col == 'P':
                    self.player = Player(self, col_index, row_index)
                    self.player.username = input_boxes[0].text  # Set the username attribute

    def new(self, input_boxes):
        # new game setups
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap(input_boxes)

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - tilesize)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + tilesize)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - tilesize, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + tilesize, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

        # Check for collisions between player attacks and enemies
        hits = pygame.sprite.groupcollide(self.attacks, self.enemies, True, True)
        for attack, enemies in hits.items():
            self.player.score += len(enemies)

        self.player.update_score()  # Update the score text

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.player.update_score()
        self.screen.blit(self.player.score_text, (10, 10))
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def gameover(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(445, 170))

        restart_button = Button(370, 230, 130, 50, WHITE, BLACK, 'Restart', 32)
        menu_button = Button(370, 290, 130, 50, WHITE, BLACK, 'Menu', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
                pygame.mixer.music.play(-1)

            if menu_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro()
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(menu_button.image, menu_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            pygame.mixer.music.stop()

    def intro(self):
        intro = True

        title = self.font.render('Traveller', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 80, 100, 50, WHITE, BLACK, 'Play', 30)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                pygame.mixer.music.play(-1)

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def SQl_menu(self):
        menu = True
        login_button = Button(10, 80, 100, 50, WHITE, BLACK, 'Login', 30)
        register_button = Button(10, 180, 140, 50, WHITE, BLACK, 'Register', 30)

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Quit all pygame windows
                    sys.exit()  # Exit the program

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if login_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
                login()

            if register_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
                registration()

            self.screen.blit(login_button.image, login_button.rect)
            self.screen.blit(register_button.image, register_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()

input_boxes = [InputBox(100, 100, 140, 32), InputBox(100, 200, 140, 32)]
g.SQl_menu()
g.intro()
g.new(input_boxes)
g.main()
g.gameover()

pygame.quit()
sys.exit()