import random

import Globals
import pygame
from GameElements.Enemies.AnimatedEnemy import AnimatedEnemy, Gun
from GameElements.Enemies.EnemyAI import *


class Stage:
    def __init__(self, not_spawned_enemies):
        self.not_spawned_enemies = not_spawned_enemies
        self.enemies = pygame.sprite.Group()

    def update(self):
        if len(self.not_spawned_enemies) != 0:
            enemy = self.not_spawned_enemies.pop()
            Globals.game.addEnemy(enemy)
            self.enemies.add(enemy)

    def finished(self):
        return len(self.not_spawned_enemies) == 0 and not bool(self.enemies)


class Level:

    def __init__(self):
        self.background = Globals.resourceManager.get_image("2.png")
        self.cloud = Globals.resourceManager.get_image("cloud.png")

        self.enemies = [Globals.resourceManager.get_sprite_sheet("enemy1.png"),
                        Globals.resourceManager.get_sprite_sheet("enemy2.png"),
                        Globals.resourceManager.get_sprite_sheet("enemy3.png")]
        self.level_progress = 0
        self.stage = None

    def Start(self):
        self.level_progress = 0
        self.stage = None
        y = 0
        while y < Globals.game.screen_size[1]:
            Globals.game.addBackground(self.background).rect.top = y
            y += self.background.get_height()

    def random_x(self, width):
        return random.randint(width, Globals.game.screen_size[0] - width)

    def create_enemy(self, enemy_id, pos=None):
        if pos is None:
            center = (self.random_x(self.enemies[enemy_id].get_width()), 0)

        if enemy_id == 0:
            return AnimatedEnemy(self.enemies[0], EnemyAIFlyby(), center, hp=20, guns=[Gun(shoot_delay=30)])
        elif enemy_id == 1:
            return AnimatedEnemy(self.enemies[1], EnemyAIHover(), center, hp=30, guns=[Gun(gun_type=6, shoot_delay=50, bullet_speed=6)])
        elif enemy_id == 2:
            return AnimatedEnemy(self.enemies[2], EnemyAIHover(), center, hp=200, max_speed=0.5,
                                 guns=[
                                     Gun(gun_type=9, shoot_delay=20, bullet_speed=6, special_offset=(-0.45, 0.95)),
                                     Gun(gun_type=9, shoot_delay=20, bullet_speed=6, special_offset=(0.45, 0.95))
                                 ])
        else:
            return None



    def Update(self):
        move = 1

        if self.stage is None or self.stage.finished():
            enemy1 = self.create_enemy(2)
            enemy2 = self.create_enemy(0)
            enemy2.ai = EnemyAIFormation(enemy1)
            self.stage = Stage([enemy1, enemy2, self.create_enemy(1), self.create_enemy(1)])

        self.stage.update()

        # Background
        if self.level_progress % self.background.get_height() == 0:
            Globals.game.addBackground(self.background)

        if self.level_progress % 500 == 0:
            Globals.game.addForeground(self.cloud)

        self.level_progress += move

        return move
