import math
import random
from dataclasses import dataclass


@dataclass
class Bolt:
    ids: list[int]
    proc_chance: float
    effect_value: float

    def roll_damage(self, max_hit, hp):
        return


class RubyBolts(Bolt):
    def roll_damage(self, max_hit, hp):
        return int(min(500 * self.effect_value, math.floor(hp * (1 + self.effect_value))))


class DiamondBolts(Bolt):
    def roll_damage(self, max_hit, hp):
        actual_max_hit = math.floor(max_hit * (1 + self.effect_value))
        return int(random.random() * (actual_max_hit + 1))


RUBY_BOLTS = RubyBolts([9242, 21944], 0.06, 0.2)
DIAMOND_BOLTS = DiamondBolts([9243, 21946], 0.1, 0.15)

ALL_BOLTS = [RUBY_BOLTS, DIAMOND_BOLTS]
