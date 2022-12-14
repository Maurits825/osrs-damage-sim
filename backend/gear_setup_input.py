import copy
import math
import re

from gear_ids import BLOWPIPE
from gear_json import GearJson
from model.attack_style.attack_style import AttackStyle
from model.boost import Boost, BoostType
from model.condition import Condition, ConditionVariables, ConditionComparison
from model.input_setup import GearSetup, InputSetup
from model.locations import Location
from model.npc.combat_stats import CombatStats
from model.prayer import Prayer, PrayerMultiplier
from model.weapon_stats import WeaponStats
from weapon import Weapon
from weapons.custom_weapons import CUSTOM_WEAPONS
from weapons.weapon_loader import WeaponLoader
from wiki_data import WikiData


class GearSetupInput:
    @staticmethod
    def load_gear_setup(name: str, attack_style_name: str, prayers: [Prayer] = None,
                        boosts: [Boost] = [], combat_stats: CombatStats = None, attacks: int = math.inf, is_special=False) -> GearSetup:
        gear_dict = GearJson.load_gear()
        gear = gear_dict[name]

        total_gear_stats = WeaponStats(name=name)
        weapon = None
        for gear_id in gear:
            weapon_stats = WikiData.get_item(gear_id)
            total_gear_stats += weapon_stats

            # TODO this could be moved higher up like in damage_sim.py?
            if weapon_stats.weapon_category:
                attack_style: AttackStyle = weapon_stats.weapon_category.value[0]
                for style in weapon_stats.weapon_category.value:
                    if re.match(attack_style_name + " \\(", style.name):
                        attack_style = style

                if weapon_stats.name in CUSTOM_WEAPONS:
                    weapon = copy.deepcopy(CUSTOM_WEAPONS[weapon_stats.name])
                else:
                    weapon = Weapon()

                weapon.set_attack_style_and_speed(attack_style, weapon_stats.attack_speed)

                total_gear_stats.id = weapon_stats.id

                if is_special:
                    weapon.set_is_special_attack(is_special)

        # TODO calc boosted stats here?
        combat_stats_copy = copy.deepcopy(combat_stats)
        for boost in boosts:
            boost.apply_boost(combat_stats_copy)

        return GearSetup(name=name,
                         gear_stats=total_gear_stats,
                         weapon=weapon,
                         attack_count=attacks,
                         prayers=prayers,
                         boosts=boosts,
                         combat_stats=combat_stats_copy,
                         gear=dict(), #TODO
                         is_fill=False,
                         conditions=[])

    @staticmethod
    def get_input_setup(json_data) -> InputSetup:
        npc = WikiData.get_npc(json_data["npc"])

        if npc.location == Location.TOMBS_OF_AMASCUT:
            raid_level = json_data.get("raidLevel")
            path_level = json_data.get("pathLevel")

            path_level_mult = 0.08 if path_level > 0 else 0.05
            npc.combat_stats.hitpoints = int(
                round(npc.combat_stats.hitpoints / 10 * (1 + raid_level * 0.004) * (
                            1 + (path_level - 1) * 0.05 + path_level_mult) * json_data["teamSize"], 0) * 10
            )
        else:
            raid_level = None
            path_level = None

        setups = []
        for setup in json_data["gearInputSetups"]:
            gear_setups = []
            for gear_setup in setup:
                attack_count = math.inf if gear_setup["attackCount"] == 0 else gear_setup["attackCount"]
                prayers = [Prayer[prayer.upper()] for prayer in gear_setup["prayers"]]

                boosts = [Boost(BoostType[boost.upper()]) for boost in gear_setup["boosts"]]
                combat_stats = CombatStats(99, gear_setup["combatStats"]["attack"], gear_setup["combatStats"]["strength"],
                                           99, gear_setup["combatStats"]["magic"], gear_setup["combatStats"]["ranged"])

                for boost in boosts:
                    boost.apply_boost(combat_stats)

                total_gear_stats = WeaponStats(name=gear_setup["name"])
                gear = {"id": gear_setup["gear"], "name": []}
                for gear_id in gear_setup["gear"]:
                    weapon_stats = WikiData.get_item(gear_id)
                    gear["name"].append(weapon_stats.name.lower())
                    total_gear_stats += weapon_stats

                weapon_item = WikiData.get_item(gear_setup["weapon"])
                weapon = WeaponLoader.load_weapon(weapon_item)

                if weapon_item.id == BLOWPIPE:
                    total_gear_stats.ranged_strength += WikiData.get_item(gear_setup["blowpipeDarts"]).ranged_strength

                total_gear_stats.id = weapon_item.id

                attack_style = weapon_item.weapon_category.value[0]
                for style in weapon_item.weapon_category.value:
                    if gear_setup["attackStyle"] == style.name:
                        attack_style = style

                conditions = [Condition(ConditionVariables[condition["variable"]],
                                        ConditionComparison[condition["comparison"]],
                                        condition["value"], ConditionComparison[condition["nextComparison"]])
                              for condition in gear_setup["conditions"]]

                weapon.initialize(attack_style=attack_style, attack_speed=weapon_item.attack_speed,
                                  combat_stats=combat_stats, prayer=PrayerMultiplier.sum_prayers(prayers),
                                  total_gear_stats=total_gear_stats, raid_level=raid_level,
                                  is_special_attack=gear_setup["isSpecial"],
                                  special_attack_cost=WikiData.get_special_attack(weapon_item.name), npc=npc,
                                  gear=gear, is_on_slayer_task=gear_setup["isOnSlayerTask"],
                                  is_in_wilderness=gear_setup["isInWilderness"],
                                  max_hp=gear_setup["maxHp"], current_hp=gear_setup["currentHp"],
                                  mining_lvl=gear_setup["miningLvl"]
                                  )

                gear_setups.append(
                    GearSetup(
                        name=gear_setup["name"],
                        gear_stats=total_gear_stats,
                        weapon=weapon,
                        attack_count=attack_count,
                        prayers=prayers,
                        boosts=boosts,
                        combat_stats=combat_stats,
                        gear=gear,
                        is_fill=gear_setup["isFill"],
                        conditions=conditions
                    )
                )

            setups.append(gear_setups)

        return InputSetup(
            npc=npc,
            gear_setups=setups,
            raid_level=raid_level,
            path_level=path_level,
        )
