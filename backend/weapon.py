from __future__ import annotations

import math
import random

from bolt_special_attack import BoltSpecialAttack
from constants import TICK_LENGTH
from dps_calculator import DpsCalculator
from input_setup.special_gear_bonus import SpecialGearBonus
from input_setup.gear_ids import (TRIDENT_SWAMP, SHADOW_STAFF, SANG_STAFF, CHAOS_GAUNTLETS, BRIMSTONE, TRIDENT_SEAS,
                                  DAWNBRINGER, HARM_STAFF)
from model.attack_style.attack_type import AttackType
from model.attack_style.combat_style import CombatStyle
from model.bolt import Bolt
from model.combat_boost import CombatBoost
from model.gear_setup import GearSetup
from model.locations import Location
from model.npc.combat_stats import CombatStats
from model.npc.npc_stats import NpcStats
from model.prayer import PrayerMultiplier
from wiki_data import WikiData


class Weapon:
    MELEE_TYPES = [AttackType.STAB, AttackType.SLASH, AttackType.CRUSH]

    def __init__(self, gear_setup: GearSetup, combat_stats: CombatStats,  npc: NpcStats, raid_level):
        self.gear_setup = gear_setup
        self.combat_stats = combat_stats
        self.npc = npc
        self.raid_level = raid_level

        self.special_attack_cost = WikiData.get_special_attack(gear_setup.gear_stats.name)
        self.prayer_multiplier = PrayerMultiplier.sum_prayers(self.gear_setup.prayers)

        self.damage_multiplier = SpecialGearBonus.get_damage_multiplier(
            self.gear_setup.equipped_gear, self.npc, self.gear_setup.current_hp,
            self.combat_stats.hitpoints, self.gear_setup.mining_lvl
        )

        self.special_bolt: Bolt | None = BoltSpecialAttack.get_equipped_special_bolt(
            self.gear_setup.equipped_gear,
            self.gear_setup.is_kandarin_diary,
        )

        self.void_bonus: CombatBoost() = SpecialGearBonus.get_gear_void_bonuses(self.gear_setup.equipped_gear)
        self.special_gear_bonus: CombatBoost() = SpecialGearBonus.get_gear_bonus(
            self.gear_setup.equipped_gear, self.gear_setup.attack_style, self.gear_setup.is_on_slayer_task,
            self.gear_setup.is_in_wilderness, self.npc, self.gear_setup.spell
        )

        self.is_brimstone = self.get_is_brimstone()
        self.set_attack_speed()

        self.max_hit = 0
        self.attack_roll = 0
        self.target_defence = None
        self.target_defence_style = None
        self.update_max_hit_and_attack_roll()

    def set_npc(self, npc):
        self.npc = npc

    def set_combat_stats(self, combat_stats):
        self.combat_stats = combat_stats
        self.update_max_hit_and_attack_roll()

    def update_max_hit_and_attack_roll(self):
        self.max_hit = self.get_max_hit()
        self.attack_roll = self.get_attack_roll()
        self.target_defence, self.target_defence_style = self.get_npc_defence_style()

    def get_is_brimstone(self):
        return (self.gear_setup.attack_style.attack_type == AttackType.MAGIC and
                BRIMSTONE in self.gear_setup.equipped_gear.ids)

    def set_attack_speed(self):
        if self.gear_setup.attack_style.combat_style == CombatStyle.RAPID:
            self.gear_setup.gear_stats.attack_speed -= 1

        if self.gear_setup.spell:
            self.gear_setup.gear_stats.attack_speed = 5

            if (HARM_STAFF in self.gear_setup.equipped_gear.ids and
                    self.gear_setup.spell in WikiData.get_standard_spells()):
                self.gear_setup.gear_stats.attack_speed = 4

    def roll_hit(self) -> bool:
        attack_roll = int(random.random() * (self.attack_roll + 1))
        defence_roll = int(random.random() * (self.get_defence_roll() + 1))

        return attack_roll > defence_roll

    def roll_damage(self) -> int:
        if self.special_bolt:
            bolt_damage = BoltSpecialAttack.roll_damage(
                self.special_bolt, self.max_hit, self.npc.combat_stats.hitpoints
            )
            if bolt_damage:
                return bolt_damage

        damage = 0
        if self.roll_hit():
            damage = int(random.random() * (self.max_hit + 1))

        return math.floor(damage * self.damage_multiplier)

    def get_accuracy(self):
        attack_roll = self.get_attack_roll()
        defence_roll = self.get_average_defence_roll()

        return DpsCalculator.get_hit_chance(attack_roll, defence_roll)

    def get_max_hit(self):
        if self.gear_setup.attack_style.attack_type in Weapon.MELEE_TYPES:
            effective_melee_str = DpsCalculator.get_effective_melee_str(
                prayer=self.prayer_multiplier,
                strength_lvl=self.combat_stats.strength,
                attack_style_boost=self.gear_setup.attack_style.combat_style.value.strength,
                melee_void_boost=self.void_bonus.melee.strength_boost[-1]
            )
            gear_melee_strength = self.gear_setup.gear_stats.melee_strength
            return DpsCalculator.get_melee_max_hit(effective_melee_str, gear_melee_strength,
                                                   self.special_gear_bonus.melee.strength_boost)
        elif self.gear_setup.attack_style.attack_type == AttackType.RANGED:
            effective_ranged_str = DpsCalculator.get_effective_ranged_str(
                prayer=self.prayer_multiplier,
                ranged_lvl=self.combat_stats.ranged,
                attack_style_boost=self.gear_setup.attack_style.combat_style.value.ranged,
                ranged_void_boost=self.void_bonus.ranged.strength_boost[-1]
            )
            gear_ranged_strength = self.gear_setup.gear_stats.ranged_strength
            return DpsCalculator.get_ranged_max_hit(effective_ranged_str, gear_ranged_strength,
                                                    self.special_gear_bonus.ranged.strength_boost)
        elif self.gear_setup.attack_style.attack_type == AttackType.MAGIC:
            return self.get_magic_max_hit()

    def get_defence_roll(self):
        defence_roll = DpsCalculator.get_defence_roll(self.target_defence[0], self.target_defence_style)

        if self.is_brimstone:
            brimstone_roll = random.randint(1, 4)
            if brimstone_roll == 1:
                defence_roll -= max(0, math.floor(defence_roll * 0.1))

        if self.raid_level:
            defence_roll = math.floor(defence_roll * (1 + (self.raid_level * 0.004)))

        return defence_roll

    def get_average_defence_roll(self):
        target_defence, target_defence_style = self.get_npc_defence_style()
        defence_roll = DpsCalculator.get_defence_roll(target_defence[0], target_defence_style)

        if self.is_brimstone:
            defence_roll -= math.floor(defence_roll * 0.1) / 4

        if self.raid_level:
            defence_roll = defence_roll * (1 + (self.raid_level * 0.004))

        return math.floor(defence_roll)

    def get_npc_defence_style(self) -> ([int], int):
        target_defence = []
        target_defence_style = 0

        if self.gear_setup.attack_style.attack_type in Weapon.MELEE_TYPES:
            target_defence = [self.npc.combat_stats.defence]
            if self.gear_setup.attack_style.attack_type == AttackType.STAB:
                target_defence_style = self.npc.defensive_stats.stab
            elif self.gear_setup.attack_style.attack_type == AttackType.SLASH:
                target_defence_style = self.npc.defensive_stats.slash
            elif self.gear_setup.attack_style.attack_type == AttackType.CRUSH:
                target_defence_style = self.npc.defensive_stats.crush
        elif self.gear_setup.attack_style.attack_type == AttackType.RANGED:
            target_defence = [self.npc.combat_stats.defence]
            target_defence_style = self.npc.defensive_stats.ranged
        elif self.gear_setup.attack_style.attack_type == AttackType.MAGIC:
            target_defence = [self.npc.combat_stats.magic]
            target_defence_style = self.npc.defensive_stats.magic

        return target_defence, target_defence_style

    def get_attack_roll(self):
        effective_skill_attack_lvl = 0
        gear_skill_bonus = 0
        gear_attack_bonus = 1

        if self.gear_setup.attack_style.attack_type in Weapon.MELEE_TYPES:
            gear_attack_bonus = self.special_gear_bonus.melee.attack_boost
            effective_skill_attack_lvl = DpsCalculator.get_effective_melee_attack(
                prayer=self.prayer_multiplier,
                attack_lvl=self.combat_stats.attack,
                attack_style_boost=self.gear_setup.attack_style.combat_style.value.attack,
                void_boost=self.void_bonus.melee.attack_boost[-1]
            )

            if self.gear_setup.attack_style.attack_type == AttackType.STAB:
                gear_skill_bonus = self.gear_setup.gear_stats.stab
            elif self.gear_setup.attack_style.attack_type == AttackType.SLASH:
                gear_skill_bonus = self.gear_setup.gear_stats.slash
            elif self.gear_setup.attack_style.attack_type == AttackType.CRUSH:
                gear_skill_bonus = self.gear_setup.gear_stats.crush

        elif self.gear_setup.attack_style.attack_type == AttackType.RANGED:
            gear_attack_bonus = self.special_gear_bonus.ranged.attack_boost
            effective_skill_attack_lvl = DpsCalculator.get_effective_ranged_attack(
                prayer=self.prayer_multiplier,
                ranged_lvl=self.combat_stats.ranged,
                attack_style_boost=self.gear_setup.attack_style.combat_style.value.ranged,
                void_boost=self.void_bonus.ranged.attack_boost[-1]
            )
            gear_skill_bonus = self.gear_setup.gear_stats.ranged
        elif self.gear_setup.attack_style.attack_type == AttackType.MAGIC:
            gear_attack_bonus = self.special_gear_bonus.magic.attack_boost
            effective_skill_attack_lvl = DpsCalculator.get_effective_magic_level(
                prayer=self.prayer_multiplier,
                magic_lvl=self.combat_stats.magic,
                attack_style_boost=self.gear_setup.attack_style.combat_style.value.magic,
                void_boost=self.void_bonus.magic.attack_boost[-1]
            )
            if self.gear_setup.gear_stats.id in SHADOW_STAFF:
                shadow_mult = 4 if self.npc.location == Location.TOMBS_OF_AMASCUT else 3
                gear_skill_bonus = self.gear_setup.gear_stats.magic * shadow_mult
            else:
                gear_skill_bonus = self.gear_setup.gear_stats.magic

        return DpsCalculator.get_attack_roll(effective_skill_attack_lvl, gear_skill_bonus, gear_attack_bonus)

    def get_dps(self):
        accuracy = self.get_accuracy()
        max_hit = self.get_max_hit()

        if self.special_bolt:
            return BoltSpecialAttack.get_dps(
                self.special_bolt, accuracy, max_hit, self.gear_setup.gear_stats.attack_speed
            )

        dmg_sum = sum([math.floor(dmg * self.damage_multiplier) for dmg in range(max_hit + 1)])
        avg_dmg = dmg_sum / (max_hit + 1)
        return (avg_dmg * accuracy) / (self.gear_setup.gear_stats.attack_speed * TICK_LENGTH)

    def get_magic_max_hit(self):
        base_max_hit = self.get_magic_base_hit()

        if CHAOS_GAUNTLETS in self.gear_setup.equipped_gear.ids and "Bolt" in self.gear_setup.spell:
            base_max_hit += 3

        magic_dmg_multiplier = self.gear_setup.gear_stats.magic_strength / 100

        if self.gear_setup.gear_stats.id in SHADOW_STAFF:
            shadow_mult = 4 if self.npc.location == Location.TOMBS_OF_AMASCUT else 3
            magic_dmg_multiplier *= shadow_mult

        magic_dmg_multiplier += self.void_bonus.magic.strength_boost[-1]
        base_hit = math.floor(base_max_hit * magic_dmg_multiplier)
        max_hit = DpsCalculator.apply_gear_bonus(base_hit, self.special_gear_bonus.magic.strength_boost)
        return max_hit

    def get_magic_base_hit(self):
        if self.gear_setup.spell:
            return WikiData.get_all_spells()[self.gear_setup.spell]

        if self.gear_setup.gear_stats.id in TRIDENT_SEAS:
            return math.floor(self.combat_stats.magic / 3) - 5
        elif self.gear_setup.gear_stats.id in TRIDENT_SWAMP:
            return math.floor(self.combat_stats.magic / 3) - 2
        elif self.gear_setup.gear_stats.id in SANG_STAFF:
            return math.floor(self.combat_stats.magic / 3) - 1
        elif self.gear_setup.gear_stats.id in SHADOW_STAFF:
            return math.floor(self.combat_stats.magic / 3) + 1
        elif self.gear_setup.gear_stats.id in DAWNBRINGER:
            return math.floor(self.combat_stats.magic / 6) - 1
