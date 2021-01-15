from pygame import VIDEORESIZE, HWSURFACE, DOUBLEBUF, RESIZABLE

from GameElements.Player import *
from GameElements.Enemy import *
from GameElements.Cloud import *

import random

class Game:

    def __init__(self):
        self.screen_size = (256,320)

        self.screen = pygame.display.set_mode(self.screen_size, HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()

        self.running = False
        self.player = Player((self.screen_size[0]/2, self.screen_size[1]))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()

        self.clouds = pygame.sprite.Group();
        self.enemy_bullets = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()

        self.current_frame = 0

    def addPlayerBullet(self, bullet):
        self.player_bullets.add(bullet)
        self.all_sprites.add(bullet)

    def addEnemyBullet(self, bullet):
        self.enemy_bullets.add(bullet)
        self.all_sprites.add(bullet)

    def draw(self):
        self.fake_screen.fill((0, 125, 0))

        for entity in self.all_sprites:
            self.fake_screen.blit(entity.surf, entity.rect)

        self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0, 0))

        pygame.display.flip()

    def setScale(self, scale):
        if scale > 3:
            scale = 3

        self.screen = pygame.display.set_mode((self.screen_size[0] * scale, self.screen_size[1] * scale),
                                              HWSURFACE | DOUBLEBUF | RESIZABLE)
    def start(self):
        ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDENEMY, 1000)

        ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDCLOUD, 1200)

        clock = pygame.time.Clock()
        self.current_frame = 0
        self.running = True
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == VIDEORESIZE:
                    width, height = event.size
                    scale = int(max((width/self.screen_size[0], height / self.screen_size[1])))+1
                    self.setScale(scale)
                elif event.type == ADDENEMY:
                    new_enemy = Enemy((random.randint(0, self.screen_size[0]), 0))
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)
                elif event.type == ADDCLOUD:
                    new_cloud = Cloud()
                    self.clouds.add(new_cloud)
                    self.all_sprites.add(new_cloud)

            screen_rect = self.fake_screen.get_rect()
            pressed_keys = pygame.key.get_pressed()

            self.player.update(screen_rect, pressed_keys)
            self.player_bullets.update(screen_rect)

            self.enemies.update(screen_rect)
            self.enemy_bullets.update(screen_rect)

            self.clouds.update(screen_rect)

            self.draw()

            clock.tick(60)

            self.current_frame += 1
