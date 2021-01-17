from pygame import VIDEORESIZE, HWSURFACE, DOUBLEBUF, RESIZABLE

from GameElements.Animation import Animation
from GameElements.Player import *
from GameElements.Background import *
from GameElements.PowerUps import HealthUp
from Gui.Bar import Bar
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
        self.powerups = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()

        self.current_frame = 0
        self.camera_shake = 0

        #GUI
        self.hp_bar = Bar(pygame.Rect(5, 5, 64, 10))

    def shakeCamera(self, intensity):
        self.camera_shake = abs(self.camera_shake + intensity)

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

    def addBullet(self, bullet, player=True):
        if player:
            self.player_bullets.add(bullet)
        else:
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

        for entity in self.powerups:
            self.fake_screen.blit(entity.surf, entity.rect)

        for entity in self.all_sprites:
            self.fake_screen.blit(entity.surf, entity.rect)

        self.hp_bar.set_progress(self.player.hp/self.player.max_hp)
        self.hp_bar.draw(self.fake_screen)

        self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (self.camera_shake, 0))
        self.camera_shake = -self.camera_shake / 2

        pygame.display.flip()

    @staticmethod
    def pixel_perfect_collision(s1, s2):
        return s1.rect.colliderect(s2) and pygame.sprite.collide_mask(s1, s2)

    def check_collisions(self):

        for powerup in self.powerups:
            # Check if player picked up a powerup
            if self.player.rect.colliderect(powerup.rect):
                powerup.on_pickup(self.player)
                powerup.kill()
                Globals.resourceManager.get_sound("powerup.wav").play()

        for enemy in self.enemies:
            # Check if enemy is hit by a bullet
            for bullet in self.player_bullets:
                if self.pixel_perfect_collision(bullet, enemy):
                    enemy.damage(bullet.get_dmg())
                    bullet.kill()
                    Globals.resourceManager.get_sound("hit.wav").play()
                    self.shakeCamera(1)
            # Check if enemy is hit by the player
            if not self.player.is_invincible() and self.pixel_perfect_collision(self.player, enemy):
                self.player.damage(25)
                enemy.damage(25)
                Globals.resourceManager.get_sound("hit.wav").play()
                self.shakeCamera(5)

        if not self.player.is_invincible():
            for enemy_bullet in self.enemy_bullets:
                if self.pixel_perfect_collision(self.player, enemy_bullet):
                    self.player.damage(enemy_bullet.get_dmg())
                    enemy_bullet.kill()
                    Globals.resourceManager.get_sound("hit.wav").play()
                    self.shakeCamera(5)

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

            # update player and his bullets
            self.player.update(screen_rect, pressed_keys)
            self.player_bullets.update(screen_rect)

            # update enemies and their bullets
            self.enemies.update(screen_rect)
            self.enemy_bullets.update(screen_rect)

            # move backgrounds
            self.background.update(move, screen_rect)

            # move foreground
            self.foreground.update(move * 2, screen_rect)
            self.effects.update(move * 2, screen_rect)
            self.powerups.update(move * 2, screen_rect)

            self.check_collisions()

            self.draw()

            clock.tick(60)

            self.current_frame += 1
