from Window import Window
from Utility.ResourceManager import *

window = None
game = None
resourceManager = None

def initialize():
    global window
    global resourceManager
    global game

    resourceManager = ResourceManager("Sprites/", "Sounds/")

    resourceManager.load_sprite_sheet("explosion.png", 5, 1)
    resourceManager.load_sprite_sheet("laser-bolts.png", 2, 4)
    resourceManager.load_sprite_sheet("ship.png", 5, 2)
    resourceManager.load_sprite_sheet("enemy1.png", 2, 1)
    resourceManager.load_sprite_sheet("enemy2.png", 2, 1)
    resourceManager.load_sprite_sheet("enemy3.png", 2, 1)
    resourceManager.load_sprite_sheet("rocket.png", 2, 1)

    resourceManager.load_sprite_sheet("healthup.png", 2, 1)
    resourceManager.load_sprite_sheet("gunup.png", 2, 1)

    window = Window()
