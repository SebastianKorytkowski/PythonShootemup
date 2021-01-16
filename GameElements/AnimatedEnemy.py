import pygame

from GameElements.Animation import Animation


class AnimatedEnemy(Animation):
    def __init__(self, sprite_sheet, center=None, hp=10):
        super(AnimatedEnemy, self).__init__(sprite_sheet, center=center)
        self.speed = 2
        self.hp = hp

        # make sure enemy is hidden at the start
        self.rect.bottom = 0

    def damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def update(self, screen_rect):
        super(AnimatedEnemy, self).update()

        self.rect.move_ip(0, self.speed)
        if not self.rect.colliderect(screen_rect):
            self.kill()
