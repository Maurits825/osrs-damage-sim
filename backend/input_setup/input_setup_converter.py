import math

from constants import TOA_TEAM_SCALING, TOA_MAX_TEAM, TOB_MAX_TEAM
from input_setup.gear_ids import BLOWPIPE, UNARMED_EQUIVALENT
from model.attack_style.weapon_category import WeaponCategory
from model.boost import BoostType
from model.condition import Condition, ConditionVariables, ConditionComparison
from model.equipped_gear import EquippedGear
from model.gear_setup import GearSetup
from model.gear_slot import GearSlot
from model.input_setup.gear_setup_settings import GearSetupSettings
from model.input_setup.global_settings import GlobalSettings
from model.input_setup.input_gear_setup import InputGearSetup
from model.input_setup.input_setup import InputSetup
from model.input_setup.stat_drain import StatDrain
from model.locations import Location
from model.npc.combat_stats import CombatStats
from model.npc.npc_stats import NpcStats
from model.prayer import Prayer
from model.weapon_stats import WeaponStats
from weapons.custom_weapons import CUSTOM_WEAPONS
from weapons.weapon_loader import WeaponLoader
from wiki_data import WikiData


class InputSetupConverter:
    @staticmethod
    def get_input_setup(json_data) -> InputSetup:
        npc = WikiData.get_npc(json_data["globalSettings"]["npc"]["id"])

        # TODO maybe do this scaling in weapon or else where, also refactor when its in gear setup settings
        raid_level, path_level = InputSetupConverter.get_raid_level(npc, json_data)

        if npc.is_tob_entry_mode or npc.is_tob_normal_mode or npc.is_tob_hard_mode:
            InputSetupConverter.scale_tob_hp(npc, json_data)

        input_gear_setups = []
        for input_gear_setup in json_data["inputGearSetups"]:
            weapons = []
            gear_setup_settings = InputSetupConverter.get_gear_setup_settings(input_gear_setup["gearSetupSettings"])

            main_gear_setup, weapon_item = InputSetupConverter.get_gear_setup(input_gear_setup["mainGearSetup"])
            main_weapon = WeaponLoader.load_weapon(
                weapon_item.name, main_gear_setup, gear_setup_settings, npc, raid_level
            )

            for gear_setup_dict in input_gear_setup["fillGearSetups"]:
                gear_setup, weapon_item = InputSetupConverter.get_gear_setup(gear_setup_dict)
                weapon = WeaponLoader.load_weapon(weapon_item.name, gear_setup, gear_setup_settings, npc, raid_level)

                weapons.append(weapon)

            input_gear_setups.append(InputGearSetup(gear_setup_settings, main_weapon, weapons))

        global_settings = GlobalSettings(npc, raid_level, path_level, json_data["globalSettings"]["teamSize"],
                                         json_data["globalSettings"]["iterations"])
        return InputSetup(
            global_settings=global_settings,
            input_gear_setups=input_gear_setups,
        )

    @staticmethod
    def get_gear_setup(gear_setup) -> (GearSetup, WeaponStats):
        prayers = [Prayer[prayer.upper()] for prayer in gear_setup["prayers"]]

        gear_stats = WeaponStats(name="")
        equipped_gear = EquippedGear([], [])
        weapon_item = WikiData.get_weapon(UNARMED_EQUIVALENT)

        for gear_slot in gear_setup["gear"]:
            item = gear_setup["gear"][gear_slot]

            if not item:
                continue

            gear_id = gear_setup["gear"][gear_slot]["id"]
            weapon_stats = WikiData.get_weapon(gear_id)

            if GearSlot(gear_slot) == GearSlot.WEAPON:
                weapon_item = weapon_stats

            equipped_gear.names.append(weapon_stats.name.lower())
            equipped_gear.ids.append(gear_id)
            gear_stats += weapon_stats

        if weapon_item.id == BLOWPIPE:
            gear_stats.ranged_strength += WikiData.get_weapon(gear_setup["blowpipeDarts"]["id"]).ranged_strength

        gear_stats.id = weapon_item.id
        gear_stats.attack_speed = weapon_item.attack_speed

        if gear_setup["spell"]:
            attack_style = WeaponCategory.STAFF.value[3]
        else:
            attack_style = weapon_item.weapon_category.value[0]
            for style in weapon_item.weapon_category.value:
                if gear_setup["attackStyle"] == style.name:
                    attack_style = style

        conditions = [
            Condition(
                ConditionVariables[condition["variable"]],
                ConditionComparison[condition["comparison"]],
                condition["value"], ConditionComparison[condition["nextComparison"]]
            ) for condition in gear_setup["conditions"]
        ]

        gear_stats.name = weapon_item.name
        return GearSetup(
            name=gear_setup["setupName"],
            gear_stats=gear_stats,
            attack_style=attack_style,
            spell=gear_setup["spell"],
            prayers=prayers,
            conditions=conditions,
            equipped_gear=equipped_gear,
            is_special_attack=gear_setup["isSpecial"],
            is_on_slayer_task=gear_setup["isOnSlayerTask"],
            is_in_wilderness=gear_setup["isInWilderness"],
            current_hp=gear_setup["currentHp"],
            mining_lvl=gear_setup["miningLvl"],
            is_kandarin_diary=gear_setup["isKandarinDiary"],
        ), weapon_item

    @staticmethod
    def get_gear_setup_settings(gear_setup_settings) -> GearSetupSettings:
        stat_drains = []
        for stat_drain in gear_setup_settings["statDrains"]:
            stat_drains.append(StatDrain(CUSTOM_WEAPONS[stat_drain["name"]], stat_drain["value"]))

        boosts = [BoostType[boost.upper()] for boost in gear_setup_settings["boosts"]]
        combat_stats = CombatStats(hitpoints=gear_setup_settings["combatStats"]["hitpoints"],
                                   attack=gear_setup_settings["combatStats"]["attack"],
                                   strength=gear_setup_settings["combatStats"]["strength"],
                                   defence=99,
                                   magic=gear_setup_settings["combatStats"]["magic"],
                                   ranged=gear_setup_settings["combatStats"]["ranged"])

        return GearSetupSettings(combat_stats, boosts, stat_drains)

    @staticmethod
    def get_raid_level(npc: NpcStats, json_data):
        raid_level = None
        path_level = None

        if npc.location == Location.TOMBS_OF_AMASCUT:
            raid_level = json_data["globalSettings"].get("raidLevel")
            path_level = json_data["globalSettings"].get("pathLevel")

            path_level_mult = 0.08 if path_level > 0 else 0.05
            npc.combat_stats.hitpoints = int(
                round(npc.combat_stats.hitpoints / 10 * (1 + raid_level * 0.004) *
                      (1 + (path_level - 1) * 0.05 + path_level_mult) *
                      TOA_TEAM_SCALING[min(json_data["globalSettings"]["teamSize"], TOA_MAX_TEAM) - 1], 0) * 10
            )

        return raid_level, path_level

    @staticmethod
    def scale_tob_hp(npc: NpcStats, json_data):
        team_size = min(json_data["globalSettings"]["teamSize"], TOB_MAX_TEAM)

        if team_size == 4:
            npc.combat_stats.hitpoints = math.floor(0.875 * npc.combat_stats.hitpoints)
        elif team_size in [1, 2, 3]:
            npc.combat_stats.hitpoints = math.floor(0.75 * npc.combat_stats.hitpoints)
