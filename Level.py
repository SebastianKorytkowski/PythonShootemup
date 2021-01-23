from GameElements.Enemies.AnimatedEnemy import AnimatedEnemy, Gun, Bullets
from GameElements.Enemies.EnemyAI import *

import random

from GameStates.WinState import WinState


class Stage:
    def __init__(self, not_spawned_enemies, continue_after=50, wait_for_all_enemies_to_die=False):
        self.not_spawned_enemies = not_spawned_enemies
        self.enemies = pygame.sprite.Group()
        self.continue_after = continue_after
        self.wait_for_all_enemies_to_die = wait_for_all_enemies_to_die
        self.timer = 0

    def update(self, game):
        self.timer += 1
        if len(self.not_spawned_enemies) != 0:
            enemy = self.not_spawned_enemies.pop()
            game.addEnemy(enemy)
            self.enemies.add(enemy)

    def finished(self):
        if self.continue_after is None:
            if self.wait_for_all_enemies_to_die:
                return not bool(Globals.game.enemies)
            else:
                return len(self.not_spawned_enemies) == 0 and not bool(self.enemies)
        else:
            return self.timer >= self.continue_after


class Level:

    def __init__(self, game):
        self.game = game

        self.background = Globals.resourceManager.get_image("2.png")
        self.cloud = Globals.resourceManager.get_image("cloud.png")

        self.enemies = [Globals.resourceManager.get_sprite_sheet("enemy1.png"),
                        Globals.resourceManager.get_sprite_sheet("enemy2.png"),
                        Globals.resourceManager.get_sprite_sheet("enemy3.png"),
                        Globals.resourceManager.get_sprite_sheet("rocket.png"),
                        Globals.resourceManager.get_sprite_sheet("enemy4.png"),
                        Globals.resourceManager.get_sprite_sheet("boss.png")]
        self.level_progress = 0
        self.stage = None

        self.currentStageNr = 0

        self.stages = [
            self.SingleEnemy, *[self.SimpleWave] * 4, *[self.SniperWave, self.SimpleWave] * 4, self.TurtleWave, # First turtle
            *[self.HardWave, self.HardWave2] * 4, *[self.RushWave, self.HardWave2, self.RushWave] * 4, self.TurtleWave, # Second turle
            *[self.RushWave] * 10, self.Boss
        ]

    def Start(self):
        self.level_progress = 0
        self.stage = None
        y = 0
        while y < Globals.window.screen_size[1]:
            self.game.addBackground(self.background).rect.top = y
            y += self.background.get_height()

    def random_x(self, width):
        if Globals.window.screen_size[0] >= width*2:
            return random.randint(width, Globals.window.screen_size[0] - width)
        else:
            return Globals.window.screen_size[0]/2

    def create_enemy(self, enemy_id, posx=None):
        if posx is None:
            posx = self.random_x(self.enemies[enemy_id].get_width())

        if enemy_id == 0:
            return AnimatedEnemy(self.enemies[0], EnemyAIFlyby(), (posx, 0), hp=15, max_speed=4,
                                 guns=[Gun(shoot_delay=80)])
        elif enemy_id == 1:
            return AnimatedEnemy(self.enemies[1], EnemyAIHover(), (posx, 0), hp=40,
                                 guns=[Gun(gun_type=6, shoot_delay=60, bullet_speed=6)])
        elif enemy_id == 2:
            return AnimatedEnemy(self.enemies[2], EnemyAIHover(-24), (posx, 0), hp=1000, max_speed=0.5,
                                 guns=[
                                     Gun(gun_type=9, shoot_delay=30, bullet_speed=6, special_offset=(-0.45, 0.95)),
                                     Gun(gun_type=9, shoot_delay=30, bullet_speed=6, special_offset=(0.45, 0.95)),
                                     Gun(gun_type=Bullets.ROCKET, shoot_delay=360, special_offset=(0, 0))
                                 ])
        elif enemy_id == 3:
            return AnimatedEnemy(self.enemies[3], EnemyAISuicide(), (posx, 0), max_speed=10, hp=20, guns=[])
        elif enemy_id == 4:
            return AnimatedEnemy(self.enemies[4], EnemyAIFlyby(), (posx, 0), max_speed=7, hp=5, guns=[Gun(shoot_delay=50, bullet_speed=10)])
        elif enemy_id == 5:
            return AnimatedEnemy(self.enemies[5], EnemyAIBoss(), (posx, 0), max_speed=1, hp=7500,
                                 guns=[
                                     Gun(gun_type=9, shoot_delay=30, bullet_speed=3, special_offset=(-0.08, 0.85)),
                                     Gun(gun_type=9, shoot_delay=30, bullet_speed=3, special_offset=(0.08, 0.85)),

                                     Gun(gun_type=2, shoot_delay=100, bullet_speed=3, special_offset=(-0.15, 0.85)),
                                     Gun(gun_type=2, shoot_delay=100, bullet_speed=3, special_offset=(0.15, 0.85)),

                                     Gun(gun_type=9, shoot_delay=60, bullet_speed=3, special_offset=(-0.43, 0.7)),
                                     Gun(gun_type=9, shoot_delay=60, bullet_speed=3, special_offset=(0.43, 0.7)),

                                     Gun(gun_type=4, shoot_delay=60, bullet_speed=3, special_offset=(-0.65, 0.85)),
                                     Gun(gun_type=4, shoot_delay=60, bullet_speed=3, special_offset=(0.65, 0.85)),
                                 ])
        else:
            return None

    def Update(self, game_not_paused=True):
        move = 1

        if game_not_paused:
            if self.stage is None or self.stage.finished():
                if len(self.stages) > self.currentStageNr >= 0:
                    self.stage = self.stages[self.currentStageNr]()
                    self.currentStageNr += 1
                else:
                    Globals.window.change_game_state(WinState(Globals.game))

            self.stage.update(self.game)

        # Background
        if self.level_progress % self.background.get_height() == 0:
            self.game.addBackground(self.background)

        if self.level_progress % 500 == 0:
            self.game.addForeground(self.cloud)

        self.level_progress += move

        return move

    def SingleEnemy(self):
        return Stage([self.create_enemy(0)], continue_after=None)

    def SimpleWave(self):
        return Stage([self.create_enemy(0, 30), self.create_enemy(0, Globals.window.screen_size[0] - 30)])

    def SniperWave(self):
        return Stage([self.create_enemy(0, 30), self.create_enemy(1, Globals.window.screen_size[0] / 2),
                      self.create_enemy(0, Globals.window.screen_size[0] - 30)], continue_after=None)

    def TurtleWave(self):
        return Stage([self.create_enemy(2)], continue_after=None)

    def HardWave(self):
        return Stage([self.create_enemy(0, 30), self.create_enemy(0, Globals.window.screen_size[0] / 2),
                      self.create_enemy(0, Globals.window.screen_size[0] - 30), self.create_enemy(4), self.create_enemy(4), self.create_enemy(4)])

    def HardWave2(self):
        return Stage([self.create_enemy(0, 30), self.create_enemy(1, Globals.window.screen_size[0] / 2),
                      self.create_enemy(0, Globals.window.screen_size[0] - 30), self.create_enemy(4), self.create_enemy(4), self.create_enemy(4)], continue_after=None)

    def RushWave(self):
        return Stage([self.create_enemy(4), self.create_enemy(4), self.create_enemy(4), self.create_enemy(4), self.create_enemy(4), self.create_enemy(4)])


    def Boss(self):
        return Stage([self.create_enemy(5)], continue_after=None, wait_for_all_enemies_to_die=True)
