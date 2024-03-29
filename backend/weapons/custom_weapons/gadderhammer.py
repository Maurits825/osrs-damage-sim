import math
import random

from constant import TICK_LENGTH
from model.damage_sim_results.special_proc import SpecialProc
from weapons.weapon import Weapon

DOUBLE_DMG_CHANCE = 0.05
AVG_DMG_BOOST = 1.2875  # from wiki


class Gadderhammer(Weapon):
    def roll_damage(self):
        damage = 0
        max_hit = self.max_hit
        roll_hit = self.roll_hit()
        if roll_hit:
            damage = int(random.random() * (self.max_hit + 1))

            double_hit = random.random()
            if double_hit <= DOUBLE_DMG_CHANCE:
                self.hitsplat.special_procs.append(SpecialProc.GADDERHAMMER)
                damage = math.floor(damage * 2 * self.damage_multiplier)  # TODO is base dmg x2 or after its floored?
                max_hit = self.max_hit * 2 * self.damage_multiplier
            else:
                damage = math.floor(damage * self.damage_multiplier)

        self.hitsplat.set_hitsplat(damage=damage, hitsplats=damage, roll_hits=roll_hit,
                                   accuracy=self.accuracy, max_hits=max_hit)

    def get_dps(self):
        accuracy = self.get_accuracy()
        max_hit = self.get_max_hit()

        avg_dmg = sum([math.floor(dmg * AVG_DMG_BOOST) for dmg in range(max_hit + 1)]) / (max_hit + 1)
        return (avg_dmg * accuracy) / (self.gear_setup.gear_stats.attack_speed * TICK_LENGTH)
