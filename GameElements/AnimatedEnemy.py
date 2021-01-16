import pygame

from GameElements.Animation import Animation
from GameElements.Damageable import Damageable


class AnimatedEnemy(Animation, Damageable):
    def __init__(self, sprite_sheet, center=None, hp=10):
        Animation.__init__(self, sprite_sheet, center=center)
        Damageable.__init__(self, hp)

        self.speed = 2

        # make sure enemy is hidden at the start
        self.rect.bottom = 0

    def update(self, screen_rect):
        self.updateAnim()

        self.rect.move_ip(0, self.speed)
        if not self.rect.colliderect(screen_rect):
            self.kill()
