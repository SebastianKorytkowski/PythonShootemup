from GameElements.Enemies.AnimatedEnemy import AnimatedEnemy, Gun, Bullets
from GameElements.Enemies.EnemyAI import *

import random


class Stage:
    def __init__(self, not_spawned_enemies, continue_after=50):
        self.not_spawned_enemies = not_spawned_enemies
        self.enemies = pygame.sprite.Group()
        self.continue_after = continue_after
        self.timer = 0

    def update(self, game):
        self.timer += 1
        if len(self.not_spawned_enemies) != 0:
            enemy = self.not_spawned_enemies.pop()
            game.addEnemy(enemy)
            self.enemies.add(enemy)

    def finished(self):
        if self.continue_after is None:
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
                        Globals.resourceManager.get_sprite_sheet("rocket.png")]
        self.level_progress = 0
        self.stage = None

        self.currentStageNr = 0

        self.stages = [self.Stage1, *[self.Stage2] * 4, *[self.Stage3, self.Stage2] * 4, self.Stage4]

    def Start(self):
        self.level_progress = 0
        self.stage = None
        y = 0
        while y < Globals.window.screen_size[1]:
            self.game.addBackground(self.background).rect.top = y
            y += self.background.get_height()

    def random_x(self, width):
        return random.randint(width, Globals.window.screen_size[0] - width)

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
            return AnimatedEnemy(self.enemies[2], EnemyAIHover(), (posx, 0), hp=1000, max_speed=0.5,
                                 guns=[
                                     Gun(gun_type=9, shoot_delay=30, bullet_speed=6, special_offset=(-0.45, 0.95)),
                                     Gun(gun_type=9, shoot_delay=30, bullet_speed=6, special_offset=(0.45, 0.95)),
                                     Gun(gun_type=Bullets.ROCKET, shoot_delay=360, special_offset=(0, 0))
                                 ])
        elif enemy_id == 3:
            return AnimatedEnemy(self.enemies[3], EnemyAISuicide(), (posx, 0), max_speed=10, hp=20, guns=[])
        else:
            return None

    def Update(self, player_alive=True):
        move = 1

        if player_alive:
            if self.stage is None or self.stage.finished():
                self.stage = self.stages[self.currentStageNr]()
                self.currentStageNr += 1
                if self.currentStageNr >= len(self.stages):
                    self.currentStageNr = 0

        self.stage.update(self.game)

        # Background
        if self.level_progress % self.background.get_height() == 0:
            self.game.addBackground(self.background)

        if self.level_progress % 500 == 0:
            self.game.addForeground(self.cloud)

        self.level_progress += move

        return move

    def Stage1(self):
        return Stage([self.create_enemy(0)])

    def Stage2(self):
        return Stage([self.create_enemy(0, 30), self.create_enemy(0, Globals.window.screen_size[0] - 30)])

    def Stage3(self):
        return Stage([self.create_enemy(0, 30), self.create_enemy(1, Globals.window.screen_size[0] / 2),
                      self.create_enemy(0, Globals.window.screen_size[0] - 30)])

    def Stage4(self):
        return Stage([self.create_enemy(2)], continue_after=None)
