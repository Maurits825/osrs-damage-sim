import math
import random

from dps_calculator import DpsCalculator
from weapon import Weapon


class Scythe(Weapon):
    def roll_damage(self) -> int:
        damage = self.roll_single_hit(1)

        if self.npc.size > 1:
            damage += self.roll_single_hit(0.5)
        if self.npc.size > 2:
            damage += self.roll_single_hit(0.25)

        return damage

    def roll_single_hit(self, reduction) -> int:
        damage = 0
        if self.roll_hit():
            damage = random.randint(0, self.max_hit)

        return math.floor(damage * reduction)

    def get_dps(self):
        accuracy = self.get_accuracy()
        max_hit = self.get_max_hit()

        effective_max_hit = max_hit
        if self.npc.size > 1:
            effective_max_hit += math.floor(max_hit * 0.5)
        if self.npc.size > 2:
            effective_max_hit += math.floor(max_hit * 0.25)

        return DpsCalculator.get_dps(effective_max_hit, accuracy, self.gear_setup.gear_stats.attack_speed)
