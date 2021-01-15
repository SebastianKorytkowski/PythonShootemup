from Game import *
from Utility.SpriteManager import *

game = None
spriteManager = None

def initialize():
    global game
    global spriteManager
    game = Game()
    spriteManager = SpriteManager("Sprites/")

    spriteManager.load_sprite_sheet("explosion.png", 5, 1)
    spriteManager.load_sprite_sheet("laser-bolts.png", 2, 2)
