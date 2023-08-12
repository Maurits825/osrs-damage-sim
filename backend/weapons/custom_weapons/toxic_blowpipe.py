import math

from weapons.weapon import Weapon


class ToxicBlowpipe(Weapon):
    def get_attack_roll(self):
        if self.gear_setup.is_special_attack:
            return super().get_attack_roll() * 2
        else:
            return super().get_attack_roll()

    def get_max_hit(self) -> int | list[int]:
        max_hit = super().get_max_hit()
        if self.gear_setup.is_special_attack:
            return math.floor(max_hit * 1.5)
        else:
            return max_hit
