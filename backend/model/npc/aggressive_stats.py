from dataclasses import dataclass


@dataclass()
class AggressiveStats:
    attack: int = 0
    magic: int = 0
    ranged: int = 0

    melee_strength: int = 0
    ranged_strength: int = 0
    magic_strength: int = 0
