import pygame
import Globals
from Utility.SpriteSheet import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, center=None, bullet_type=0, is_player=False):
        super(Bullet, self).__init__()

        if is_player:
            if bullet_type <= 0 or bullet_type > 3:
                bullet_type = 0
            self.surf = Globals.resourceManager.get_sprite_sheet("laser-bolts.png").images[bullet_type]
        else:
            if bullet_type <= 0 or bullet_type > 3:
                bullet_type = 0
            self.surf = Globals.resourceManager.get_sprite_sheet("laser-bolts.png").images[4+bullet_type]

        self.rect = self.surf.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.surf)
        self.speed = speed
        self.bullet_type = bullet_type

    def get_dmg(self):
        return {
            0: 5,
            1: 10,
            2: 15,
            3: 20,
        }.get(self.bullet_type, 0)

    def update(self, screen_rect):
        self.rect.move_ip(self.speed)
        if not self.rect.colliderect(screen_rect):
            self.kill()
