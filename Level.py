import random

import Globals
from GameElements.Enemies.AnimatedEnemy import AnimatedEnemy
from GameElements.Enemies.EnemyAI import *


class Level:

    def __init__(self):
        self.background = Globals.resourceManager.get_image("2.png")
        self.cloud = Globals.resourceManager.get_image("cloud.png")

        self.enemies = [Globals.resourceManager.get_sprite_sheet("enemy1.png"),
                       Globals.resourceManager.get_sprite_sheet("enemy2.png"),
                       Globals.resourceManager.get_sprite_sheet("enemy3.png")]
        self.level_progress = 0

    def Start(self):
        self.level_progress = 0
        y = 0
        while y < Globals.game.screen_size[1]:
            Globals.game.addBackground(self.background).rect.top = y
            y += self.background.get_height()

    def random_x(self, width):
        return random.randint(width, Globals.game.screen_size[0] - width)

    def spawn_enemy(self, id, pos = None):
        if pos is None:
            center = (self.random_x(self.enemies[id].get_width()), 0)


        if id == 0:
            Globals.game.addEnemy(AnimatedEnemy(self.enemies[0], EnemyAIFollow(), center, hp=20))
        elif id == 1:
            Globals.game.addEnemy(AnimatedEnemy(self.enemies[1], EnemyAIFollow(), center, hp=30))
        elif id == 2:
            Globals.game.addEnemy(AnimatedEnemy(self.enemies[2], EnemyAIFollow(), center, hp=100))
        else:
            print("Wrong enemy id: " + str(id))

    def Update(self):
        move = 1

        if self.level_progress % self.background.get_height() == 0:
            Globals.game.addBackground(self.background)

        if self.level_progress % 500 == 0:
            Globals.game.addForeground(self.cloud)

        if self.level_progress % 33 == 0:
            self.spawn_enemy(0)

        self.level_progress += move

        return move
