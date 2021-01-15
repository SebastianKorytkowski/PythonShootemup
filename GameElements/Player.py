import Globals
from GameElements.Bullet import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, center=None):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=center)

        self.shoot_previous_frame = 0
        self.shoot_delay_frames = 5

    def update(self, screen_rect, pressed_keys):
        speed = 2

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)

        # Let player shoot bullets!
        if pressed_keys[pygame.K_SPACE]:
            if Globals.game.current_frame - self.shoot_previous_frame > self.shoot_delay_frames:
                self.shoot_previous_frame = Globals.game.current_frame
                new_bullet = Bullet((0,-3), (self.rect.centerx, self.rect.top), bullet_type=Globals.game.current_frame%4)
                Globals.game.addPlayerBullet(new_bullet)


        # Don't let player move outside of the map
        self.rect.clamp_ip(screen_rect)
