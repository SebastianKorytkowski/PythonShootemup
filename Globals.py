from Game import *
from Utility.ResourceManager import *

game = None
resourceManager = None

def initialize():
    global game
    global resourceManager
    resourceManager = ResourceManager("Sprites/", "Sounds/")

    resourceManager.load_sprite_sheet("explosion.png", 5, 1)
    resourceManager.load_sprite_sheet("laser-bolts.png", 2, 4)
    resourceManager.load_sprite_sheet("ship.png", 5, 2)
    resourceManager.load_sprite_sheet("enemy1.png", 2, 1)
    resourceManager.load_sprite_sheet("enemy2.png", 2, 1)
    resourceManager.load_sprite_sheet("enemy3.png", 2, 2)
    resourceManager.load_sprite_sheet("rocket.png", 2, 1)

    resourceManager.load_sprite_sheet("healthup.png", 2, 1)

    game = Game()
