import math

from constants import TICK_LENGTH
from model.prayer import PrayerMultiplier


class DpsCalculator:
    @staticmethod
    def get_effective_melee_str(prayer: PrayerMultiplier, strength_lvl, attack_style_boost, melee_void_boost):
        return math.floor((math.floor(strength_lvl * prayer.strength) +
                           attack_style_boost + 8) * melee_void_boost)

    @staticmethod
    def get_effective_ranged_str(prayer: PrayerMultiplier, ranged_lvl, attack_style_boost, ranged_void_boost):
        return math.floor((math.floor(ranged_lvl * prayer.ranged_strength) +
                           attack_style_boost + 8) * ranged_void_boost)

    @staticmethod
    def get_effective_melee_attack(prayer: PrayerMultiplier, attack_lvl, attack_style_boost, void_boost):
        return math.floor((math.floor(attack_lvl * prayer.attack) +
                           attack_style_boost + 8) * void_boost)

    @staticmethod
    def get_effective_ranged_attack(prayer: PrayerMultiplier, ranged_lvl, attack_style_boost, void_boost):
        return math.floor((math.floor(ranged_lvl * prayer.ranged) +
                           attack_style_boost + 8) * void_boost)

    @staticmethod
    def get_melee_max_hit(effective_melee_str, gear_melee_strength, gear_bonus):
        base_hit = math.floor(((effective_melee_str * (gear_melee_strength + 64)) + 320) / 640)
        return DpsCalculator.apply_gear_bonus(base_hit, gear_bonus)

    @staticmethod
    def get_ranged_max_hit(effective_ranged_str, gear_ranged_strength, gear_bonus):
        base_hit = math.floor(0.5 + ((effective_ranged_str * (gear_ranged_strength + 64)) / 640))
        return DpsCalculator.apply_gear_bonus(base_hit, gear_bonus)

    @staticmethod
    def apply_gear_bonus(base_value, gear_bonus):
        new_value = base_value
        for bonus in gear_bonus:
            new_value = math.floor(new_value * bonus)

        return new_value

    @staticmethod
    def get_effective_magic_level(prayer: PrayerMultiplier, magic_lvl, attack_style_boost, void_boost):
        return math.floor((math.floor(magic_lvl * prayer.magic) * void_boost) + attack_style_boost + 9)

    @staticmethod
    def get_attack_roll(effective_skill_lvl, gear_skill_bonus, gear_bonus):
        attack_roll = math.floor(effective_skill_lvl * (gear_skill_bonus + 64))
        return DpsCalculator.apply_gear_bonus(attack_roll, gear_bonus)

    @staticmethod
    def get_defence_roll(target_defence, target_defence_style):
        return (target_defence + 9) * (target_defence_style + 64)

    @staticmethod
    def get_hit_chance(attack_roll, defence_roll):
        if attack_roll > defence_roll:
            return 1 - ((defence_roll + 2) / (2 * (attack_roll + 1)))
        else:
            return attack_roll / (2 * (defence_roll + 1))

    @staticmethod
    def get_dps(max_hit, hit_chance, attack_speed):
        return ((max_hit * hit_chance) / 2) / (attack_speed * TICK_LENGTH)
