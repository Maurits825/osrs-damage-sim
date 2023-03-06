from __future__ import annotations

import math

import numpy as np

from constants import TICK_LENGTH
from model.boost import BoostType
from model.damage_sim_results import TotalDamageSimData, DamageSimResults, InputGearSetupLabels
from model.input_setup.gear_setup_settings import GearSetupSettings
from model.input_setup.global_settings import GlobalSettings
from model.input_setup.input_gear_setup import InputGearSetup
from model.input_setup.stat_drain import StatDrain
from model.npc.combat_stats import CombatStats
from model.sim_stats import SimStats, TimeSimStats
from model.stat_drain_type import StatDrainType
from weapon import Weapon
from weapons.arclight import Arclight
from weapons.bandos_godsword import BandosGodsword
from weapons.dragon_warhammer import DragonWarhammer

BOOST_NAME = {
    BoostType.SMELLING_SALTS: "Salt",
    BoostType.SUPER_ATTACK: "Super att",
    BoostType.SUPER_STRENGTH: "Super str",
    BoostType.SUPER_COMBAT: "SCP",
    BoostType.RANGING: "Ranged",
    BoostType.LIQUID_ADRENALINE: "Adrenaline",
    BoostType.OVERLOAD_PLUS: "Overload+",
}

STAT_DRAIN_NAME = {
    DragonWarhammer: "DWH",
    BandosGodsword: "BGS",
    Arclight: "Arclight",
}

STAT_DRAIN_TYPE = {
    StatDrainType.DAMAGE: "dmg",
    StatDrainType.HITS: "hits",
}

MAX_COMBAT_STATS = 99


class DamageSimStats:
    @staticmethod
    def get_data_stats(data) -> SimStats:
        np_data = np.array(data)
        average = np.average(np_data)
        maximum = np.max(np_data)
        minimum = np.min(np_data)

        cumulative_sum = DamageSimStats.get_cumulative_sum(data)
        chance_to_kill = [
            int(np.argmax(cumulative_sum >= 0.25)),
            int(np.argmax(cumulative_sum >= 0.50)),
            int(np.argmax(cumulative_sum >= 0.75))
        ]

        try:
            frequent = int(np.argmax(np.bincount(np_data)))
        except TypeError:
            frequent = 0

        return SimStats(float(average), int(maximum), int(minimum), int(frequent), list(chance_to_kill))

    @staticmethod
    def get_ticks_stats(sim_stats: SimStats) -> TimeSimStats:
        return TimeSimStats(
            DamageSimStats.format_ticks_to_time(sim_stats.average),
            DamageSimStats.format_ticks_to_time(sim_stats.maximum),
            DamageSimStats.format_ticks_to_time(sim_stats.minimum),
            DamageSimStats.format_ticks_to_time(sim_stats.most_frequent),
            [DamageSimStats.format_ticks_to_time(chance) for chance in sim_stats.chance_to_kill],
        )

    @staticmethod
    def get_data_2d_stats(data_list2d) -> list[SimStats]:
        sim_stats_list = []
        data_list = []
        for index in range(len(data_list2d[0])):
            for data in data_list2d:
                data_list.append(data[index])

            sim_stats_list.append(DamageSimStats.get_data_stats(data_list))
            data_list.clear()
        return sim_stats_list

    @staticmethod
    def print_ticks_stats(stats: SimStats, label: str):
        text = label + ": Average: " + DamageSimStats.format_ticks_to_time(stats.average) + ", " + \
               "Frequent: " + DamageSimStats.format_ticks_to_time(stats.most_frequent) + ", " + \
               "Max: " + DamageSimStats.format_ticks_to_time(stats.maximum) + ", " + \
               "Min: " + DamageSimStats.format_ticks_to_time(stats.minimum) + ", " + \
               "25%: " + DamageSimStats.format_ticks_to_time(stats.chance_to_kill[0]) + ", " + \
               "50%: " + DamageSimStats.format_ticks_to_time(stats.chance_to_kill[1]) + ", " + \
               "75%: " + DamageSimStats.format_ticks_to_time(stats.chance_to_kill[2])

        print(text)

    @staticmethod
    def print_stats(stats: SimStats, label: str):
        text = label + ": Average: " + str(round(stats.average, 4)) + ", " + \
               "Frequent: " + str(round(stats.most_frequent, 4)) + ", " + \
               "Max: " + str(round(stats.maximum, 4)) + ", " + \
               "Min: " + str(round(stats.minimum, 4))
        print(text)

    @staticmethod
    def format_ticks_to_time(ticks):
        total_seconds = ticks * TICK_LENGTH
        minutes = math.floor(total_seconds / 60)
        seconds = round(total_seconds % 60, 1)

        seconds_str = ("0" + str(seconds))[-4:]
        return str(minutes) + ":" + seconds_str

    @staticmethod
    def get_cumulative_sum(data):
        bin_count = np.bincount(data) / len(data)
        return np.cumsum(bin_count)

    @staticmethod
    def print_setup(weapon_setups: list[Weapon], total_damage_stats: list[SimStats]):
        text = ""
        for idx, weapon in enumerate(weapon_setups):
            text += weapon.gear_setup.name
            text += ", Avg Total Damage: " + str(round(total_damage_stats[idx].average, 1))

            text += ", DPS: " + str(round(weapon.get_dps(), 4)) + "\n"

        print(text[:-1])

    @staticmethod
    def get_input_gear_setup_label(input_gear_setup: InputGearSetup) -> InputGearSetupLabels:
        gear_setup_settings_label = DamageSimStats.get_gear_setup_settings_label(input_gear_setup.gear_setup_settings)
        all_weapon_labels = DamageSimStats.get_all_weapons_label(input_gear_setup.all_weapons)

        input_gear_setup_label = gear_setup_settings_label + " -> "
        for weapon_label in all_weapon_labels:
            input_gear_setup_label += weapon_label + ", "

        return InputGearSetupLabels(input_gear_setup_label[:-2], gear_setup_settings_label, all_weapon_labels)

    @staticmethod
    def get_all_weapons_label(all_weapons: list[Weapon]) -> list[str]:
        weapon_labels = []
        for weapon in all_weapons:
            weapon_labels.append(DamageSimStats.get_weapon_label(weapon))
        return weapon_labels

    @staticmethod
    def get_weapon_label(weapon: Weapon) -> str:
        label = ""
        gear = weapon.gear_setup
        prayer_and_boost_text = ""
        for prayer in gear.prayers:
            prayer_and_boost_text += prayer.name.lower().capitalize() + ", "

        if prayer_and_boost_text:
            prayer_and_boost_text = " (" + prayer_and_boost_text[:-2] + ")"

        label = label + (gear.name or "unnamed") + prayer_and_boost_text
        return label

    @staticmethod
    def get_gear_setup_settings_label(gear_setup_settings: GearSetupSettings) -> str:
        gear_setup_settings_label = ""
        combat_stats_text = DamageSimStats.get_combat_stats_label(gear_setup_settings.combat_stats)
        boost_text = DamageSimStats.get_boost_label(gear_setup_settings.boosts)
        stat_drain_text = DamageSimStats.get_stat_drain_label(gear_setup_settings.stat_drains)

        for text in [combat_stats_text, boost_text, stat_drain_text]:
            if text:
                gear_setup_settings_label += text + " | "

        return gear_setup_settings_label[:-2]

    @staticmethod
    def get_stat_drain_label(stat_drains: list[StatDrain]) -> str | None:
        stat_drain_text = ""
        for stat_drain in stat_drains:
            stat_drain_text += (STAT_DRAIN_NAME[stat_drain.weapon] + ": " + str(stat_drain.value) + " " +
                                STAT_DRAIN_TYPE[stat_drain.weapon.stat_drain_type] + ", ")

        if stat_drain_text:
            return "Stat drain - " + stat_drain_text[:-2]

        return None

    @staticmethod
    def get_boost_label(boosts: list[BoostType]) -> str | None:
        boost_text = ""
        for boost in boosts:
            boost_text += BOOST_NAME.get(boost, str(boost.name).replace('_', ' ').lower()) + ", "

        if boost_text:
            return "Boosts - " + boost_text[:-2]

        return None

    @staticmethod
    def get_combat_stats_label(combat_stats: CombatStats) -> str | None:
        stats_text = ""

        if combat_stats.hitpoints != MAX_COMBAT_STATS:
            stats_text += "hp: " + str(combat_stats.hitpoints) + ", "

        if combat_stats.attack != MAX_COMBAT_STATS:
            stats_text += "att: " + str(combat_stats.attack) + ", "

        if combat_stats.strength != MAX_COMBAT_STATS:
            stats_text += "str: " + str(combat_stats.strength) + ", "

        if combat_stats.defence != MAX_COMBAT_STATS:
            stats_text += "def: " + str(combat_stats.defence) + ", "

        if combat_stats.magic != MAX_COMBAT_STATS:
            stats_text += "magic: " + str(combat_stats.magic) + ", "

        if combat_stats.ranged != MAX_COMBAT_STATS:
            stats_text += "ranged: " + str(combat_stats.ranged) + ", "

        if stats_text:
            return "Combat stats - " + stats_text[:-2]

        return None

    @staticmethod
    def get_graph_title_info(global_settings: GlobalSettings):
        title = (global_settings.npc.name +
                 " | HP: " +
                 str(global_settings.npc.base_combat_stats.hitpoints))

        if global_settings.raid_level:
            title += " | raid level: " + str(global_settings.raid_level)
            if global_settings.path_level:
                title += ", path level: " + str(global_settings.path_level)

        title += " | iterations: " + f"{global_settings.iterations:,}"

        return title

    @staticmethod
    def populate_damage_sim_results(damage_sim_results: DamageSimResults, sim_data: TotalDamageSimData) -> SimStats:

        ttk_stats = DamageSimStats.get_data_stats(sim_data.ticks_to_kill)
        damage_sim_results.ttk_stats.append(DamageSimStats.get_ticks_stats(ttk_stats))

        sim_dps_stats = DamageSimStats.get_data_2d_stats(sim_data.gear_dps)
        damage_sim_results.sim_dps_stats.append(sim_dps_stats)

        total_damage_stats = DamageSimStats.get_data_2d_stats(sim_data.gear_total_dmg)
        damage_sim_results.total_damage_stats.append(total_damage_stats)

        attack_count_stats = DamageSimStats.get_data_2d_stats(sim_data.gear_attack_count)
        damage_sim_results.attack_count_stats.append(attack_count_stats)

        damage_sim_results.cumulative_chances.append(list(DamageSimStats.get_cumulative_sum(sim_data.ticks_to_kill)))

        return ttk_stats

    @staticmethod
    def get_min_and_max_ticks(ttk_stats: list[SimStats]):
        min_ticks = math.inf
        max_ticks = 0

        for ttk_stat in ttk_stats:
            min_ticks = min(min_ticks, ttk_stat.minimum)
            max_ticks = max(max_ticks, ttk_stat.maximum)

        return min_ticks, max_ticks
