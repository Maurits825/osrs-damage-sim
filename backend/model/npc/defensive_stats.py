from dataclasses import dataclass


@dataclass()
class DefensiveStats:
    stab: int = 0
    slash: int = 0
    crush: int = 0
    magic: int = 0
    ranged: int = 0
