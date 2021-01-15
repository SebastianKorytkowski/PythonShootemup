import Globals

class Level:

    def __init__(self):
        self.background = Globals.spriteManager.get_image("1.png")
        self.cloud = Globals.spriteManager.get_image("cloud.png")

    def Start(self):
        y = 0
        while y < Globals.game.screen_size[1]:
            Globals.game.addBackground(self.background).rect.top = y
            y += self.background.get_height();


    def Update(self):
        frame = Globals.game.current_frame

        if frame % self.background.get_height() == 0:
            Globals.game.addBackground(self.background)

        if frame % 500 == 0:
            Globals.game.addBackground(self.cloud)


        return 1

