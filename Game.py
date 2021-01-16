from pygame import VIDEORESIZE, HWSURFACE, DOUBLEBUF, RESIZABLE

from GameElements.Animation import Animation
from GameElements.Player import *
from GameElements.Background import *
from Level import *

import random


class Game:

    def __init__(self):
        self.screen_size = (256, 320)

        self.screen = pygame.display.set_mode(self.screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.fake_screen = self.screen.copy()

        self.running = False
        self.player = Player((self.screen_size[0] / 2, self.screen_size[1]))

        self.level = Level()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()

        self.background = pygame.sprite.Group()
        self.foreground = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()

        self.current_frame = 0
        self.camera_shake = 0

    def addEnemy(self, new_enemy):
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def spawnExplosion(self, position):
        new_explosion = Animation(Globals.resourceManager.get_sprite_sheet("explosion.png"), center=position,
                                  loop=False, frames_per_frame=5)
        self.effects.add(new_explosion)

    def addBackground(self, image) -> Background:
        new_background = Background(image)
        self.background.add(new_background)
        return new_background

    def addForeground(self, image) -> Background:
        new_foreground = Background(image)
        self.foreground.add(new_foreground)
        return new_foreground

    def addPlayerBullet(self, bullet):
        self.player_bullets.add(bullet)
        self.all_sprites.add(bullet)

    def addEnemyBullet(self, bullet):
        self.enemy_bullets.add(bullet)
        self.all_sprites.add(bullet)

    def setScale(self, scale):
        if scale > 3:
            scale = 3

        self.screen = pygame.display.set_mode((self.screen_size[0] * scale, self.screen_size[1] * scale),
                                              HWSURFACE | DOUBLEBUF | RESIZABLE)

    def draw(self):
        for entity in self.background:
            self.fake_screen.blit(entity.surf, entity.rect)

        for entity in self.foreground:
            self.fake_screen.blit(entity.surf, entity.rect)

        for entity in self.effects:
            self.fake_screen.blit(entity.surf, entity.rect)

        for entity in self.all_sprites:
            self.fake_screen.blit(entity.surf, entity.rect)

        self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (self.camera_shake,0))
        self.camera_shake = -self.camera_shake / 2

        pygame.display.flip()

    def check_collisions(self):

        for enemy in self.enemies:
            for bullet in self.player_bullets:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.damage(4):# Enemy has died from this bullet
                        self.spawnExplosion(enemy.rect.center)
                        Globals.resourceManager.get_sound("explosion.wav").play()
                        self.camera_shake = 2
                    bullet.kill()
                    Globals.resourceManager.get_sound("hit.wav").play()
                    self.camera_shake = 1

            if self.player.rect.colliderect(enemy.rect):
                self.spawnExplosion(enemy.rect.center)
                Globals.resourceManager.get_sound("explosion.wav").play()
                enemy.kill()
                self.camera_shake = 5



    def start(self):

        clock = pygame.time.Clock()
        self.current_frame = 0
        self.running = True

        self.level.Start()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == VIDEORESIZE:
                    width, height = event.size
                    scale = int(max((width / self.screen_size[0], height / self.screen_size[1]))) + 1
                    self.setScale(scale)

            move = self.level.Update()
            screen_rect = self.fake_screen.get_rect()
            pressed_keys = pygame.key.get_pressed()

            self.player.update(screen_rect, pressed_keys)
            self.player_bullets.update(screen_rect)

            self.enemies.update(screen_rect)
            self.enemy_bullets.update(screen_rect)

            self.background.update(move, screen_rect)
            self.foreground.update(move * 2, screen_rect)

            self.effects.update()

            self.check_collisions()

            self.draw()

            clock.tick(60)

            self.current_frame += 1
