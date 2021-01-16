import pygame

import Globals
from GameElements.Animation import Animation
from GameElements.Player import Player


class GunUp(Animation):
    def __init__(self, position):
        sprite_sheet = Globals.resourceManager.get_sprite_sheet("gunup.png")
        Animation.__init__(self, sprite_sheet, center=position, loop=True, frames_per_frame=10)

    def on_pickup(self, player: Player):
        player.gun.gun_type.upgrade()


class HealthUp(Animation):
    def __init__(self, position):
        sprite_sheet = Globals.resourceManager.get_sprite_sheet("healthup.png")
        Animation.__init__(self, sprite_sheet, center=position, loop=True, frames_per_frame=10)

    def on_pickup(self, player: Player):
        player.heal(50)