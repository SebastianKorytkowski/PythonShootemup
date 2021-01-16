import random

from GameElements.BaseClasses.Damageable import Damageable
from GameElements.BaseClasses.PhysicsBase import PhysicsBase
from GameElements.PowerUps import *
from GameElements.Gun import *
from GameElements.Enemies.EnemyAI import *


class AnimatedEnemy(Animation, Damageable, PhysicsBase):
    def __init__(self, sprite_sheet, center=None, hp=10, ai=EnemyAIFollow()):
        Animation.__init__(self, sprite_sheet, center=center)
        Damageable.__init__(self, hp)

        self.gun = Gun(shoot_delay=30)
        self.max_speed = 2
        self.ai = ai

        # make sure enemy is hidden at the start
        self.rect.bottom = 0

        PhysicsBase.__init__(self)

    def update(self, screen_rect):
        self.updateAnim()

        self.gun.shoot((self.rect.centerx, self.rect.bottom), False)

        self.speed = self.ai.move_direction(self)*self.max_speed

        self.update_physics()
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def on_death(self):
        for i in range(0, random.randint(1, 3)):
            Globals.game.spawnExplosion((random.uniform(self.rect.left, self.rect.right), (random.uniform(self.rect.top, self.rect.bottom))))

        if random.uniform(0.0, 1.0) > 0.9:
            Globals.game.powerups.add(HealthUp(self.rect.center))

        if random.uniform(0, 1) > 0.95:
            Globals.game.powerups.add(GunUp(self.rect.center))

        Globals.game.shakeCamera(5)
        Globals.resourceManager.get_sound("explosion.wav").play()
