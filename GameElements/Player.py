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

        self.shoot_previous_frame = 0
        self.shoot_delay_frames = 5
        self.speed_vector = [0, 0]

        self.acceleration = 1
        self.inertia = 0.69
        self.maxspeed = 5

        self.animationCounter = 0

        self.setFrame()
        self.rect = self.surf.get_rect(center=center)

    def setFrame(self):

        dir = self.speed_vector[0]/self.maxspeed

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

        self.speed_vector[0] = self.clamp(input[0]*self.acceleration + self.speed_vector[0] * self.inertia, -self.maxspeed, self.maxspeed)
        self.speed_vector[1] = self.clamp(input[1]*self.acceleration + self.speed_vector[1] * self.inertia, -self.maxspeed, self.maxspeed)

        self.rect.move_ip(self.speed_vector[0], self.speed_vector[1])

        self.setFrame()
        if Globals.game.current_frame % 10 == 0:
            if self.animationCounter == 0:
                self.animationCounter = 1
            else:
                self.animationCounter = 0

        # Let player shoot bullets!
        if pressed_keys[pygame.K_SPACE]:
            if Globals.game.current_frame - self.shoot_previous_frame > self.shoot_delay_frames:
                self.shoot_previous_frame = Globals.game.current_frame
                new_bullet = Bullet((0, -5), (self.rect.centerx, self.rect.top), bullet_type=0)
                Globals.game.addPlayerBullet(new_bullet)
                Globals.resourceManager.get_sound("shot-heavy.wav").play()


        # Don't let player move outside of the map
        self.rect.clamp_ip(screen_rect)
