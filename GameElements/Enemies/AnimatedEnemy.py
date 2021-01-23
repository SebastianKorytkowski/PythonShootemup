import random

from GameElements.BaseClasses.Damageable import Damageable
from GameElements.BaseClasses.PhysicsBase import PhysicsBase
from GameElements.PowerUps import *
from GameElements.Gun import *
from GameElements.Enemies.EnemyAI import *


class AnimatedEnemy(Animation, Damageable, PhysicsBase):
    def __init__(self, sprite_sheet, ai, position=None, hp=10, max_speed=2, guns=[Gun(shoot_delay=30)]):
        Animation.__init__(self, sprite_sheet, center=position)
        Damageable.__init__(self, hp)

        self.rect.bottom = position[1]

        self.guns = guns
        self.max_speed = max_speed
        self.ai = ai

        PhysicsBase.__init__(self)

    def update(self, screen_rect):
        self.updateAnim()

        for gun in self.guns:
            gun.shoot(self, False)

        self.speed = (self.speed*5.0 + self.ai.move_direction(self)*self.max_speed)/7.0

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

        Globals.game.score += self.max_hp*self.max_hp;

        Globals.window.shakeCamera(5)
        Globals.resourceManager.get_sound("explosion.wav").play()
