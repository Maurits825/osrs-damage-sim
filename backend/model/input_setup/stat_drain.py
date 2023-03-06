from dataclasses import dataclass

from model.stat_drain_weapon import StatDrainWeapon


@dataclass()
class StatDrain:
    weapon: StatDrainWeapon
    value: int
