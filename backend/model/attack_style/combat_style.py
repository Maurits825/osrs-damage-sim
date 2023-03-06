from aenum import Enum, NoAlias
from dataclasses import dataclass


@dataclass()
class CombatStyleBoost:
    attack: int = 0
    strength: int = 0
    ranged: int = 0
    magic: int = 0


class CombatStyle(Enum):
    _settings_ = NoAlias

    ACCURATE = CombatStyleBoost(attack=3, ranged=3, magic=2)
    AGGRESSIVE = CombatStyleBoost(strength=3)
    CONTROLLED = CombatStyleBoost(attack=1, strength=1)
    RAPID = CombatStyleBoost()
    DEFENSIVE = CombatStyleBoost()
    LONGRANGE = CombatStyleBoost()
    AUTOCAST = CombatStyleBoost()
