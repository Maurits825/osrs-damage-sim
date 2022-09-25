from damage_sim_stats import DamageSimStats
from gear_setup_input import GearSetupInput
from model.boost import BoostType, Boost
from model.combat_stats import CombatStats
from model.input_setup import InputSetup, GearSetup
from model.prayer import Prayer, PrayerMultiplier
from weapon import Weapon
from wiki_data import WikiData
from dataclasses import dataclass


@dataclass()
class DamageSimData:
    ticks_to_kill: int
    weapon_damages: dict


class DamageSim:
    def __init__(self):
        self.wiki_data = WikiData()

        self.input_setup = None

    def get_input_setup(self) -> InputSetup:
        # first get inputs
        # TODO get npc by name
        npc = self.wiki_data.get_npc(11730)  # Zebak
        # TODO better way? - this is input, none boosted stats
        combat_stats = CombatStats(99, 99, 99, 99, 99, 99)
        # TODO as input maybe or something, list or setup names
        # TODO prayer input here?
        gear_setups = [
            [
                GearSetupInput.load_gear_setup("Max ZCB", "Rapid", [Prayer.RIGOUR], 2, True),
                GearSetupInput.load_gear_setup("Max dragon claws", "Slash", [Prayer.PIETY], 1, True),
                GearSetupInput.load_gear_setup("Max Tbow", "Rapid", [Prayer.RIGOUR])
            ],
            [
                GearSetupInput.load_gear_setup("Max ZCB", "Rapid", [Prayer.RIGOUR], 1, True),
                GearSetupInput.load_gear_setup("Max dragon claws", "Slash", [Prayer.PIETY], 2, True),
                GearSetupInput.load_gear_setup("Max Tbow", "Rapid", [Prayer.RIGOUR])
            ],
            [
                GearSetupInput.load_gear_setup("Max dragon claws", "Slash", [Prayer.PIETY], 4, True),
                GearSetupInput.load_gear_setup("Max Tbow", "Rapid", [Prayer.RIGOUR])
            ],
        ]
        # TODO boosts and prayer input
        boosts = [Boost(BoostType.SMELLING_SALTS)]

        # TODO input for this
        raid_level = 0
        path_level = 0

        # TODO calc boosted stats here?
        for boost in boosts:
            boost.apply_boost(combat_stats)

        # TODO set cmb stats,prayers & gear bonus here?
        for gear_setup in gear_setups:
            for gear in gear_setup:
                gear.weapon.set_combat_stats(combat_stats)
                if gear.prayers:
                    gear.weapon.set_prayer(PrayerMultiplier.sum_prayers(gear.prayers))
                gear.weapon.set_total_gear_stats(gear.gear_stats)

                gear.weapon.update_attack_roll()
                gear.weapon.update_max_hit()
                gear.weapon.set_raid_level(raid_level)

        return InputSetup(
            npc=npc,
            combat_stats=combat_stats,
            gear_setups=gear_setups,
            boosts=boosts,
            raid_level=raid_level,
            path_level=path_level
        )

    def run(self, iterations):
        self.input_setup = self.get_input_setup()

        max_ticks = 0
        for gear_setup in self.input_setup.gear_setups:
            ticks_to_kill, weapon_sim_dps = self.run_simulator(iterations, gear_setup)
            ttk_stats = DamageSimStats.get_data_stats(ticks_to_kill)
            sim_dps_stats = DamageSimStats.get_data_2d_stats(weapon_sim_dps)

            DamageSimStats.print_setup(gear_setup)
            for idx, dps in enumerate(sim_dps_stats):
                DamageSimStats.print_stats(dps, gear_setup[idx].name + " Sim DPS")
            DamageSimStats.print_ticks_stats(ttk_stats, "Time")
            print("")

            max_ticks = max(max_ticks, ttk_stats.maximum)
            DamageSimStats.graph_n_cumulative_tick_count(ticks_to_kill, gear_setup)

        DamageSimStats.show_cumulative_graph(max_ticks, self.input_setup)

    def run_simulator(self, iterations, gear_setup: [GearSetup]) -> [DamageSimData]:
        ticks_to_kill_list = []
        weapon_sim_dps_list = []
        for i in range(iterations):
            ticks_to_kill, weapon_sim_dps = self.run_damage_sim(gear_setup)
            ticks_to_kill_list.append(ticks_to_kill)
            weapon_sim_dps_list.append(weapon_sim_dps)

        return ticks_to_kill_list, weapon_sim_dps_list

    def run_damage_sim(self, gear_setups: [GearSetup]) -> ():
        hitpoints = self.input_setup.npc.combat_stats.hitpoints
        ticks_to_kill = 0
        current_weapon_att_count = 0
        weapons_index = 0
        weapon_damages = []

        gear_setup = gear_setups[weapons_index]
        weapon: Weapon = gear_setup.weapon
        weapon_sim_dps = []
        while hitpoints > 0:
            if current_weapon_att_count >= gear_setup.attack_count:
                ticks_to_kill += current_weapon_att_count * weapon.attack_speed
                weapon_sim_dps.append(min(sum(weapon_damages), self.input_setup.npc.combat_stats.hitpoints) / (current_weapon_att_count * weapon.attack_speed * 0.6))

                current_weapon_att_count = 0
                weapon_damages.clear()

                weapons_index += 1
                gear_setup = gear_setups[weapons_index]
                weapon = gear_setup.weapon

            damage = weapon.roll_damage(hitpoints, self.input_setup.npc)
            weapon_damages.append(damage)
            hitpoints -= damage

            current_weapon_att_count += 1

        weapon_sim_dps.append(min(sum(weapon_damages), self.input_setup.npc.combat_stats.hitpoints) / (current_weapon_att_count * weapon.attack_speed * 0.6))
        # TODO by default remove the last weapon att
        ticks_to_kill += (current_weapon_att_count - 1) * weapon.attack_speed
        return ticks_to_kill, weapon_sim_dps


sim = DamageSim()
sim.run(10000)