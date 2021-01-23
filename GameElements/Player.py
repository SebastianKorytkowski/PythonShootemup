from GameElements.Bullet import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from GameElements.BaseClasses.Damageable import Damageable
from GameElements.Gun import Gun
from GameElements.BaseClasses.PhysicsBase import PhysicsBase
from GameStates.GameOverState import GameOverState


class Player(DrawableSprite, Damageable, PhysicsBase):
    def __init__(self, center=None):
        DrawableSprite.__init__(self)
        Damageable.__init__(self, 100)

        self.acceleration = 1
        self.inertia = 0.69
        self.max_speed = 5

        self.gun = Gun(bullet_speed=5)
        self.hp = 100

        self.animationCounter = 0

        self.invincibility_till_frame = 60

        self.speed = pygame.Vector2(0, 0)
        self.setFrame()
        self.rect = self.surf.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.surf)

        PhysicsBase.__init__(self)

        self.invisible_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.invisible_surf.fill((255, 255, 255, 0))

    def setFrame(self):
        # Make player flash when invincible
        if self.is_invincible() and Globals.window.current_frame % 2 == 0 and Globals.window.current_frame != 0:
            self.surf = self.invisible_surf
            return

        dir = self.speed.x / self.max_speed

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

    def is_invincible(self):
        return Globals.window.current_frame <= self.invincibility_till_frame

    def on_damage(self, dmg):
        # Give invincibility for 30 frames after getting dmg
        self.invincibility_till_frame = Globals.window.current_frame + 10

    def on_death(self):
        Globals.window.change_game_state(GameOverState(Globals.window.game_state))

    def update(self, screen_rect, pressed_keys):

        input = pygame.Vector2(0, 0)
        if pressed_keys[K_UP]:
            input.y -= 1
        if pressed_keys[K_DOWN]:
            input.y += 1
        if pressed_keys[K_LEFT]:
            input.x -= 1
        if pressed_keys[K_RIGHT]:
            input.x += 1

        self.speed.x = self.clamp(input.x * self.acceleration + self.speed.x * self.inertia,
                                  -self.max_speed, self.max_speed)
        self.speed.y = self.clamp(input.y * self.acceleration + self.speed.y * self.inertia,
                                  -self.max_speed, self.max_speed)

        self.update_physics()

        self.setFrame()
        if Globals.window.current_frame % 10 == 0:
            if self.animationCounter == 0:
                self.animationCounter = 1
            else:
                self.animationCounter = 0

        # Let player shoot bullets!
        if pressed_keys[pygame.K_SPACE]:
            self.gun.shoot(self, True)

        # Don't let player move outside of the map
        if not screen_rect.contains(self.rect):
            self.rect.clamp_ip(screen_rect)
            self.pos = pygame.math.Vector2(self.rect.center)
