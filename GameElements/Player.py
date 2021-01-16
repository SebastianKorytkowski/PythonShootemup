import Globals
from GameElements.Bullet import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from GameElements.Damageable import Damageable
from GameElements.Gun import Gun


class Player(pygame.sprite.Sprite, Damageable):
    def __init__(self, center=None):
        pygame.sprite.Sprite.__init__(self)
        Damageable.__init__(self, 100)

        self.speed_vector = [0, 0]

        self.acceleration = 1
        self.inertia = 0.69
        self.max_speed = 5

        self.gun = Gun()
        self.hp = 100

        self.animationCounter = 0

        self.setFrame()
        self.rect = self.surf.get_rect(center=center)

    def setFrame(self):

        dir = self.speed_vector[0]/self.max_speed

        if dir < -0.5:
            anim_dir = 0
        elif dir < -0.25:
            anim_dir = 1
        elif dir < 0.25:
            anim_dir = 2
        elif dir < 0.5:
            anim_dir = 3
        else:
            anim_dir = 4
        self.surf = Globals.resourceManager.get_sprite_sheet("ship.png").get_at_pos(anim_dir, self.animationCounter)

    def clamp(self, x, a, b):
        return max(a, min(x, b))

    def update(self, screen_rect, pressed_keys):

        input = [0, 0]
        if pressed_keys[K_UP]:
            input[1] -= 1
        if pressed_keys[K_DOWN]:
            input[1] += 1
        if pressed_keys[K_LEFT]:
            input[0] -= 1
        if pressed_keys[K_RIGHT]:
            input[0] += 1

        self.speed_vector[0] = self.clamp(input[0] * self.acceleration + self.speed_vector[0] * self.inertia, -self.max_speed, self.max_speed)
        self.speed_vector[1] = self.clamp(input[1] * self.acceleration + self.speed_vector[1] * self.inertia, -self.max_speed, self.max_speed)

        self.rect.move_ip(self.speed_vector[0], self.speed_vector[1])

        self.setFrame()
        if Globals.game.current_frame % 10 == 0:
            if self.animationCounter == 0:
                self.animationCounter = 1
            else:
                self.animationCounter = 0

        # Let player shoot bullets!
        if pressed_keys[pygame.K_SPACE]:
            self.gun.shoot((self.rect.centerx, self.rect.top), True)


        # Don't let player move outside of the map
        self.rect.clamp_ip(screen_rect)
