
class Damageable:

    def __init__(self, max_hp, hp=None):
        self.max_hp = max_hp
        if hp is None:
            self.hp = max_hp
        else:
            self.hp = self.max_hp

    def heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
            return True
        return False
