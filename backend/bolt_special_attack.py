from __future__ import annotations

import math
import random
import copy

from constants import TICK_LENGTH
from model.bolt import ALL_BOLTS, Bolt, RubyBolts, DiamondBolts
from model.equipped_gear import EquippedGear


class BoltSpecialAttack:

    @staticmethod
    def get_equipped_special_bolt(gear: EquippedGear, is_kandarin_diary) -> Bolt | None:
        for bolt in ALL_BOLTS:
            for bolt_id in bolt.ids:
                if bolt_id in gear.ids:
                    spec_bolt = copy.deepcopy(bolt)
                    if is_kandarin_diary:
                        spec_bolt.proc_chance = spec_bolt.proc_chance * 1.1
                    return spec_bolt

        return None

    @staticmethod
    def roll_damage(bolt: Bolt, max_hit, current_hp) -> int | None:
        hit = random.random()
        if hit <= bolt.proc_chance:
            return bolt.roll_damage(max_hit, current_hp)

        return None

    @staticmethod
    def get_dps(bolt: Bolt, accuracy, max_hit, attack_speed) -> float:
        if isinstance(bolt, RubyBolts):
            spec_max_hit = math.floor(500 * bolt.effect_value)
            return ((spec_max_hit * bolt.proc_chance) +
                    ((1 - bolt.proc_chance) * accuracy * max_hit * 0.5)) / (attack_speed * TICK_LENGTH)

        elif isinstance(bolt, DiamondBolts):
            spec_max_hit = math.floor(max_hit * (1 + bolt.effect_value))
            return ((spec_max_hit * bolt.proc_chance * 0.5) +
                    ((1 - bolt.proc_chance) * accuracy * max_hit * 0.5)) / (attack_speed * TICK_LENGTH)
