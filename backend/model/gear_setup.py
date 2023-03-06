from dataclasses import dataclass

from model.attack_style.attack_style import AttackStyle
from model.condition import Condition
from model.equipped_gear import EquippedGear
from model.prayer import Prayer
from model.weapon_stats import WeaponStats


@dataclass()
class GearSetup:
    name: str
    gear_stats: WeaponStats
    attack_style: AttackStyle
    spell: str
    prayers: list[Prayer]

    conditions: list[Condition]

    equipped_gear: EquippedGear

    is_special_attack: bool
    is_on_slayer_task: bool
    is_in_wilderness: bool
    current_hp: int
    mining_lvl: int
    is_kandarin_diary: bool
