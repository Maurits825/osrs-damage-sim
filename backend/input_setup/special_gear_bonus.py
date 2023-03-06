import re

from input_setup.gear_ids import *
from model.attack_style.attack_type import AttackType
from model.combat_boost import CombatBoost
from model.equipped_gear import EquippedGear
from model.npc.npc_stats import NpcStats
from wiki_data import WikiData


class SpecialGearBonus:
    @staticmethod
    def get_gear_bonus(gear: EquippedGear, attack_style,
                       is_on_slayer_task, is_in_wilderness, npc: NpcStats, spell) -> CombatBoost:
        # gear bonus list order is important, taken as from dps calc sheet

        all_gear_names = '\t'.join(gear.names)
        special_gear_bonus = CombatBoost()

        if "bow of faerdhinen" in all_gear_names or CRYSTAL_BOW in gear.ids:
            if CRYSTAL_HELM in gear.ids or CRYSTAL_BODY in gear.ids or CRYSTAL_LEGS in gear.ids:
                crystal_att = 1
                crystal_str = 1

                if CRYSTAL_HELM in gear.ids:
                    crystal_att += 0.05
                    crystal_str += 0.025
                if CRYSTAL_BODY in gear.ids:
                    crystal_att += 0.15
                    crystal_str += 0.075
                if CRYSTAL_LEGS in gear.ids:
                    crystal_att += 0.1
                    crystal_str += 0.05

                special_gear_bonus.ranged.attack_boost.append(crystal_att)
                special_gear_bonus.ranged.strength_boost.append(crystal_str)

        # salve doesnt stack with slayer helm and overrides slayer bonus
        if any(gear_id in [SALVE, SALVE_E, SALVE_I, SALVE_EI] for gear_id in gear.ids):
            if SALVE in gear.ids:
                special_gear_bonus.melee.attack_boost.append(7 / 6)
                special_gear_bonus.melee.strength_boost.append(7 / 6)
            elif SALVE_E in gear.ids:
                special_gear_bonus.melee.attack_boost.append(1.2)
                special_gear_bonus.melee.strength_boost.append(1.2)
            elif SALVE_I in gear.ids:
                special_gear_bonus.melee.attack_boost.append(7 / 6)
                special_gear_bonus.melee.strength_boost.append(7 / 6)

                special_gear_bonus.ranged.attack_boost.append(7 / 6)
                special_gear_bonus.ranged.strength_boost.append(7 / 6)

                special_gear_bonus.magic.attack_boost.append(1.15)
                special_gear_bonus.magic.strength_boost.append(1.15)
            elif SALVE_EI in gear.ids:
                special_gear_bonus.melee.attack_boost.append(1.2)
                special_gear_bonus.melee.strength_boost.append(1.2)

                special_gear_bonus.ranged.attack_boost.append(1.2)
                special_gear_bonus.ranged.strength_boost.append(1.2)

                special_gear_bonus.magic.attack_boost.append(1.2)
                special_gear_bonus.magic.strength_boost.append(1.2)
        elif is_on_slayer_task:
            if "slayer helmet (i)" in all_gear_names or re.match(r"black mask (?:\(.*\))? ?\(i\)", all_gear_names):
                special_gear_bonus.melee.attack_boost.append(7 / 6)
                special_gear_bonus.melee.strength_boost.append(7 / 6)

                special_gear_bonus.ranged.attack_boost.append(1.15)
                special_gear_bonus.ranged.strength_boost.append(1.15)

                special_gear_bonus.magic.attack_boost.append(1.15)
                special_gear_bonus.magic.strength_boost.append(1.15)
            elif "slayer helmet" in all_gear_names or "black mask" in all_gear_names:
                special_gear_bonus.melee.attack_boost.append(7 / 6)
                special_gear_bonus.melee.strength_boost.append(7 / 6)

        if any(smoke in gear.ids for smoke in SMOKE_STAFF):
            if spell in WikiData.get_standard_spells():
                special_gear_bonus.magic.attack_boost.append(1.1)
                special_gear_bonus.magic.strength_boost.append(1.1)

        if npc.is_kalphite and "keris" in all_gear_names:
            if any(keris in gear.ids for keris in [KERIS, KERIS_PARTISAN, KERIS_SUN, KERIS_CORRUPTION]):
                special_gear_bonus.melee.strength_boost.append(1.33)
            elif KERIS_BREACHING in gear.ids:
                special_gear_bonus.melee.attack_boost.append(1.33)
                special_gear_bonus.melee.strength_boost.append(1.33)

        if npc.is_demon and ARCLIGHT in gear.ids:
            special_gear_bonus.melee.attack_boost.append(1.7)
            special_gear_bonus.melee.strength_boost.append(1.7)

        if npc.is_dragon:
            if any(dhcb in gear.ids for dhcb in DRAGON_HUNTER_CROSSBOW):
                special_gear_bonus.ranged.attack_boost.append(1.3)
                special_gear_bonus.ranged.strength_boost.append(1.25)
            elif DRAGON_HUNTER_LANCE in gear.ids:
                special_gear_bonus.melee.attack_boost.append(1.2)
                special_gear_bonus.melee.strength_boost.append(1.2)

        if is_in_wilderness:
            if CRAWS_BOW in gear.ids:
                special_gear_bonus.ranged.attack_boost.append(1.5)
                special_gear_bonus.ranged.strength_boost.append(1.5)
            elif VIGGORA_MACE in gear.ids:
                special_gear_bonus.melee.attack_boost.append(1.5)
                special_gear_bonus.melee.strength_boost.append(1.5)
            elif THAMMARON_SCEPTRE in gear.ids:
                special_gear_bonus.magic.attack_boost.append(2)
                special_gear_bonus.magic.strength_boost.append(1.25)

        if TOME_OF_WATER in gear.ids:
            if "Water" in spell:
                special_gear_bonus.magic.attack_boost.append(1.2)
                special_gear_bonus.magic.strength_boost.append(1.2)

        if TOME_OF_FIRE in gear.ids:
            if "Fire" in spell and spell in WikiData.get_standard_spells():
                special_gear_bonus.magic.strength_boost.append(1.5)

        if OBSIDIAN_ARMOUR.issubset(gear.ids):
            if any(obsidian_weapon in gear.ids for obsidian_weapon in OBSIDIAN_MELEE_WEAPONS):
                special_gear_bonus.melee.attack_boost.append(1.1)
                special_gear_bonus.melee.strength_boost.append(1.1)

        if attack_style.attack_type == AttackType.CRUSH:
            inquis_count = 0
            if INQUIS_HELM in gear.ids:
                inquis_count += 1
            if INQUIS_BODY in gear.ids:
                inquis_count += 1
            if INQUIS_LEGS in gear.ids:
                inquis_count += 1

            if inquis_count == 3:
                inquis_percent = 2.5
            else:
                inquis_percent = inquis_count * 0.5

            inquis_boost = 1 + (inquis_percent / 100)
            special_gear_bonus.melee.attack_boost.append(inquis_boost)
            special_gear_bonus.melee.strength_boost.append(inquis_boost)

        if npc.is_vampyre1 or npc.is_vampyre2 or npc.is_vampyre3:
            if IVANDIS_FLAIL in gear.ids:
                special_gear_bonus.melee.strength_boost.append(1.2)
            elif BLISTERWOOD_FLAIL in gear.ids:
                special_gear_bonus.melee.attack_boost.append(1.05)
                special_gear_bonus.melee.strength_boost.append(1.25)

        return special_gear_bonus

    @staticmethod
    def get_gear_void_bonuses(gear) -> CombatBoost:
        void_bonus = CombatBoost()

        if VOID.issubset(gear.ids):
            if MELEE_VOID in gear.ids:
                void_bonus.melee.attack_boost.append(1.1)
                void_bonus.melee.strength_boost.append(1.1)
            elif RANGED_VOID in gear.ids:
                void_bonus.ranged.attack_boost.append(1.1)
                void_bonus.ranged.strength_boost.append(1.1)
            elif MAGE_VOID in gear.ids:
                void_bonus.magic.attack_boost.append(1.45)

        elif ELITE_VOID.issubset(gear.ids):
            if MELEE_VOID in gear.ids:
                void_bonus.melee.attack_boost.append(1.1)
                void_bonus.melee.strength_boost.append(1.1)
            elif RANGED_VOID in gear.ids:
                void_bonus.ranged.attack_boost.append(1.1)
                void_bonus.ranged.strength_boost.append(1.125)
            elif MAGE_VOID in gear.ids:
                void_bonus.magic.attack_boost.append(1.45)
                void_bonus.magic.strength_boost.append(1.025)

        return void_bonus

    @staticmethod
    def get_damage_multiplier(gear: EquippedGear, npc: NpcStats, current_hp, max_hp, mining_lvl) -> float:
        if set(DHAROK_SET).issubset(gear.ids):
            return 1 + (((max_hp - current_hp) / 100) * (max_hp / 100))

        if any(b_necklace in gear.ids for b_necklace in BERSERKER_NECKLACE):
            if any(obsidian_weapon in gear.ids for obsidian_weapon in OBSIDIAN_MELEE_WEAPONS):
                return 1.2

        if npc.is_shade and GADDERHAMMER in gear.ids:
            return 1.25

        if npc.is_leafy and LEAF_BATTLE_AXE in gear.ids:
            return 1.175

        if npc.name == "Guardian":
            for pickaxe in PICKAXES:
                if pickaxe[1] in gear.ids:
                    return (50 + min(100, mining_lvl) + min(61, pickaxe[0])) / 150

        return 1
