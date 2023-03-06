import copy
import json

from model.npc.aggressive_stats import AggressiveStats
from model.npc.combat_stats import CombatStats
from model.npc.defensive_stats import DefensiveStats
from model.locations import Location
from model.npc.npc_stats import NpcStats
from model.attack_style.weapon_category import WeaponCategory
from model.weapon_stats import WeaponStats


class WikiData:
    items_json = json.load(open("./wiki_data/items-dmg-sim.json"))
    npcs_json = json.load(open("./wiki_data/npcs-dmg-sim.json"))
    unique_npcs = json.load(open("./wiki_data/unique_npcs.json"))
    extra_data = json.load(open("./wiki_data/extra_data.json"))
    gear_slot_items = json.load(open("./wiki_data/gear_slot_items.json"))
    special_attack = json.load(open("./wiki_data/special_attack.json"))
    magic_spells = json.load(open("./wiki_data/magic_spells.json"))

    @staticmethod
    def get_weapon(item_id: int) -> WeaponStats:
        weapon = WikiData.items_json[str(item_id)]
        weapon_category = None if weapon.get("weaponCategory", 0) == 0 else WeaponCategory[weapon["weaponCategory"]]
        return WeaponStats(
            name=weapon.get("name", 0),
            id=weapon.get("id", item_id),
            attack_speed=weapon.get("aspeed", 0),
            stab=weapon.get("astab", 0),
            slash=weapon.get("aslash", 0),
            crush=weapon.get("acrush", 0),
            magic=weapon.get("amagic", 0),
            ranged=weapon.get("arange", 0),
            melee_strength=weapon.get("str", 0),
            ranged_strength=weapon.get("rstr", 0),
            magic_strength=weapon.get("mdmg", 0),
            weapon_category=weapon_category,
        )

    @staticmethod
    def get_npc(npc_id: int) -> NpcStats:
        npc = WikiData.npcs_json[str(npc_id)]
        npc_name = npc["name"]
        min_defence = WikiData.extra_data["min_defence"].get(npc_name, 0)
        if npc_name in WikiData.extra_data["locations"]:
            location = Location[WikiData.extra_data["locations"][npc_name]]
        else:
            location = Location.NONE

        combat_stats = CombatStats(hitpoints=npc.get("hitpoints", 0), attack=npc.get("att", 0),
                                   strength=npc.get("str", 0), defence=npc.get("def", 0),
                                   magic=npc.get("mage", 0), ranged=npc.get("range", 0))

        return NpcStats(
            name=npc_name,
            combat_stats=combat_stats,
            base_combat_stats=copy.deepcopy(combat_stats),
            aggressive_stats=AggressiveStats(
                attack=npc.get("attbns", 0),
                magic=npc.get("amagic", 0),
                ranged=npc.get("arange", 0),
                melee_strength=npc.get("strbns", 0),
                ranged_strength=npc.get("rngbns", 0),
                magic_strength=npc.get("mbns", 0),
            ),
            defensive_stats=DefensiveStats(
                stab=npc.get("dstab", 0),
                slash=npc.get("dslash", 0),
                crush=npc.get("dcrush", 0),
                magic=npc.get("dmagic", 0),
                ranged=npc.get("drange", 0),
            ),
            min_defence=min_defence,
            location=location,
            size=npc.get("size", 0),
            is_kalphite=npc.get("isKalphite", False),
            is_demon=npc.get("isDemon", False),
            is_dragon=npc.get("isDragon", False),
            is_undead=npc.get("isUndead", False),
            is_leafy=npc.get("isLeafy", False),
            is_xerician=npc.get("isXerician", False),
            is_challenge_mode=npc.get("isChallengeMode", False),
            is_shade=npc.get("isShade", False),
            is_tob_entry_mode=npc.get("isTobEntryMode", False),
            is_tob_normal_mode=npc.get("isTobNormalMode", False),
            is_tob_hard_mode=npc.get("isTobHardMode", False),
        )

    @staticmethod
    def get_special_attack(item_name: str) -> int:
        for key in WikiData.special_attack:
            if key in item_name:
                return WikiData.special_attack[key]

        return 0

    @staticmethod
    def get_unique_npcs():
        return WikiData.unique_npcs["unique_npcs"]

    @staticmethod
    def get_all_spells():
        return WikiData.magic_spells["all_spells"]

    @staticmethod
    def get_standard_spells():
        return WikiData.magic_spells["standard_spells"]

    @staticmethod
    def get_gear_slot_items():
        return WikiData.gear_slot_items
