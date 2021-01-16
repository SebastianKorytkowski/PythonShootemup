import random

import Globals
from GameElements.AnimatedEnemy import AnimatedEnemy

class Level:

    def __init__(self):
        self.background = Globals.resourceManager.get_image("1.png")
        self.cloud = Globals.resourceManager.get_image("cloud.png")

        self.enemy1 = Globals.resourceManager.get_sprite_sheet("enemy1.png")
        self.enemy2 = Globals.resourceManager.get_sprite_sheet("enemy2.png")
        self.enemy3 = Globals.resourceManager.get_sprite_sheet("enemy3.png")

    def Start(self):
        y = 0
        while y < Globals.game.screen_size[1]:
            Globals.game.addBackground(self.background).rect.top = y
            y += self.background.get_height()


    def Update(self):
        frame = Globals.game.current_frame

        if frame % self.background.get_height() == 0:
            Globals.game.addBackground(self.background)

        if frame % 500 == 0:
            Globals.game.addForeground(self.cloud)

        if frame % 100 == 0:
            Globals.game.addEnemy(AnimatedEnemy(self.enemy1, (random.randint(0, Globals.game.screen_size[0]), 0)))

        if frame % 120 == 0:
            Globals.game.addEnemy(AnimatedEnemy(self.enemy2, (random.randint(0, Globals.game.screen_size[0]), 0)))



        return 1

