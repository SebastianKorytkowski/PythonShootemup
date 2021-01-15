import Globals
import pygame

pygame.init()

Globals.initialize()

Globals.game.setScale(2)
Globals.game.start()

pygame.quit()