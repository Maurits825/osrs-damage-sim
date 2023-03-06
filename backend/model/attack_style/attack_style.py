from dataclasses import dataclass

from model.attack_style.attack_type import AttackType
from model.attack_style.combat_style import CombatStyle


@dataclass()
class AttackStyle:
    name: str
    attack_type: AttackType
    combat_style: CombatStyle
