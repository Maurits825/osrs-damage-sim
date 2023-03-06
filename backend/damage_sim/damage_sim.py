import copy

from condition_evaluator import ConditionEvaluator
from constants import MAX_SPECIAL_ATTACK, SPEC_REGEN_TICKS, SPEC_REGEN_AMOUNT, TICK_LENGTH
from input_setup.gear_ids import LIGHTBEARER
from model.boost import BoostType, Boost
from model.damage_sim_results import SingleDamageSimData, GearSetupDpsStats
from model.input_setup.input_gear_setup import InputGearSetup
from model.npc.npc_stats import NpcStats
from model.stat_drain_type import StatDrainType
from weapon import Weapon

MAIN_WEAPON_INDEX = 0


class DamageSim:
    def __init__(self, npc: NpcStats, input_gear_setup: InputGearSetup):
        self.npc = npc

        self.main_weapon: Weapon = input_gear_setup.main_weapon
        self.fill_weapons: list[Weapon] = input_gear_setup.fill_weapons
        self.all_weapons = [self.main_weapon, *self.fill_weapons]
        self.gear_setup_settings = input_gear_setup.gear_setup_settings

        self.combat_stats = self.gear_setup_settings.combat_stats
        self.initial_combat_stats = copy.deepcopy(self.combat_stats)

        self.sim_data: SingleDamageSimData = SingleDamageSimData(0, [], [], [])

        self.current_weapon: Weapon = self.main_weapon
        self.current_weapon_index = 0

        self.special_attack = 0
        self.spec_regen_tick_timer = 0
        self.ticks_to_spec_regen = []
        self.special_attack_cost = []

        self.setup_damage_sim()

    def reset(self):
        self.current_weapon = self.main_weapon
        self.current_weapon_index = 0

        self.special_attack = MAX_SPECIAL_ATTACK
        self.spec_regen_tick_timer = 0

        self.reset_npc_combat_stats()
        self.combat_stats.set_stats(self.initial_combat_stats)

        self.sim_data = SingleDamageSimData(0, [], [], [])
        for index, _ in enumerate(self.all_weapons):
            self.sim_data.gear_total_dmg.append(0)
            self.sim_data.gear_attack_count.append(0)
            self.sim_data.gear_dps.append(0)

    def run(self) -> SingleDamageSimData:
        self.reset()

        while self.npc.combat_stats.hitpoints > 0:
            self.regenerate_special_attack()
            self.current_weapon_index, self.current_weapon = self.get_next_weapon()

            damage = self.current_weapon.roll_damage()
            self.npc.combat_stats.hitpoints -= damage

            if self.current_weapon.gear_setup.is_special_attack:
                self.special_attack -= self.special_attack_cost[self.current_weapon_index]

            self.sim_data.ticks_to_kill += self.current_weapon.gear_setup.gear_stats.attack_speed
            self.sim_data.gear_total_dmg[self.current_weapon_index] += damage
            self.sim_data.gear_attack_count[self.current_weapon_index] += 1

        # remove overkill damage
        self.sim_data.gear_total_dmg[self.current_weapon_index] += self.npc.combat_stats.hitpoints
        # remove last weapon attack time
        self.sim_data.ticks_to_kill -= self.current_weapon.gear_setup.gear_stats.attack_speed

        for index, weapon in enumerate(self.all_weapons):
            self.sim_data.gear_dps[index] = DamageSim.get_sim_dps(
                self.sim_data.gear_total_dmg[index],
                self.sim_data.gear_attack_count[index],
                weapon.gear_setup.gear_stats.attack_speed
            )

        return self.sim_data

    def get_next_weapon(self) -> tuple[int, Weapon]:
        for index, weapon in enumerate(self.fill_weapons):
            fill_weapon_index = index + 1
            use_fill_weapon = ConditionEvaluator.evaluate_condition(
                    weapon.gear_setup.conditions, self.npc.combat_stats.hitpoints,
                    self.sim_data.gear_total_dmg[fill_weapon_index],
                    self.sim_data.gear_attack_count[fill_weapon_index]
            )
            if use_fill_weapon:
                if (not weapon.gear_setup.is_special_attack or
                        (weapon.gear_setup.is_special_attack and
                         self.special_attack_cost[fill_weapon_index] <= self.special_attack)):
                    return fill_weapon_index, weapon
                else:
                    return MAIN_WEAPON_INDEX, self.main_weapon

        return MAIN_WEAPON_INDEX, self.main_weapon

    def regenerate_special_attack(self):
        if self.special_attack == MAX_SPECIAL_ATTACK:
            self.spec_regen_tick_timer = 0
            return

        self.spec_regen_tick_timer += self.current_weapon.gear_setup.gear_stats.attack_speed

        ticks_to_regen = self.ticks_to_spec_regen[self.current_weapon_index]
        if self.spec_regen_tick_timer >= ticks_to_regen:
            self.spec_regen_tick_timer -= ticks_to_regen
            self.special_attack = min(self.special_attack + SPEC_REGEN_AMOUNT, MAX_SPECIAL_ATTACK)

    def setup_damage_sim(self):
        Boost.apply_boosts(self.initial_combat_stats, self.gear_setup_settings.boosts)
        self.combat_stats.set_stats(self.initial_combat_stats)

        self.reset_npc_combat_stats()

        self.special_attack_cost = []
        for index, weapon in enumerate(self.all_weapons):
            if LIGHTBEARER in weapon.gear_setup.equipped_gear.ids:
                self.ticks_to_spec_regen.append(SPEC_REGEN_TICKS / 2)
            else:
                self.ticks_to_spec_regen.append(SPEC_REGEN_TICKS)

            if any(boost == BoostType.LIQUID_ADRENALINE for boost in self.gear_setup_settings.boosts):
                self.special_attack_cost.append(weapon.special_attack_cost / 2)
            else:
                self.special_attack_cost.append(weapon.special_attack_cost)

            weapon.set_combat_stats(self.combat_stats)

    def reset_npc_combat_stats(self):
        self.npc.combat_stats.set_stats(self.npc.base_combat_stats)

        for stat_drain in self.gear_setup_settings.stat_drains:
            if stat_drain.weapon.stat_drain_type == StatDrainType.DAMAGE:
                stat_drain.weapon.drain_stats(self.npc, stat_drain.value)
            else:
                for hit in range(stat_drain.value):
                    stat_drain.weapon.drain_stats(self.npc, 1)

    def get_weapon_dps_stats(self) -> GearSetupDpsStats:
        theoretical_dps = []
        max_hit = []
        accuracy = []
        for weapon in self.all_weapons:
            theoretical_dps.append(weapon.get_dps())
            max_hit.append(weapon.get_max_hit())
            accuracy.append(weapon.get_accuracy() * 100)

        return GearSetupDpsStats(theoretical_dps, max_hit, accuracy)

    @staticmethod
    def get_sim_dps(total_damage, attack_count, attack_speed):
        if attack_count == 0:
            return 0
        return total_damage / (attack_count * attack_speed * TICK_LENGTH)
