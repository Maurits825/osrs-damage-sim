import math

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
        return math.floor(math.floor(((effective_melee_str * (gear_melee_strength + 64)) + 320) / 640) *
                          gear_bonus)

    @staticmethod
    def get_ranged_max_hit(effective_ranged_str, gear_ranged_strength, gear_bonus):
        return math.floor(0.5 + ((effective_ranged_str * (gear_ranged_strength + 64)) / 640) * gear_bonus)

    @staticmethod
    def get_attack_roll(effective_skill_lvl, gear_skill_bonus, gear_bonus):
        return math.floor((effective_skill_lvl * (gear_skill_bonus + 64)) * gear_bonus)

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
        return ((max_hit * hit_chance) / 2) / (attack_speed * 0.6)