from dataclasses import dataclass

from model.attack_style.weapon_category import WeaponCategory


@dataclass()
class WeaponStats:
    name: str
    id: int = -1

    attack_speed: int = 0

    stab: int = 0
    slash: int = 0
    crush: int = 0
    magic: int = 0
    ranged: int = 0

    melee_strength: int = 0
    ranged_strength: int = 0
    magic_strength: int = 0

    weapon_category: WeaponCategory = None

    def __add__(self, other):
        return WeaponStats(
            name=self.name,
            stab=self.stab + other.stab,
            slash=self.slash + other.slash,
            crush=self.crush + other.crush,
            magic=self.magic + other.magic,
            ranged=self.ranged + other.ranged,
            melee_strength=self.melee_strength + other.melee_strength,
            ranged_strength=self.ranged_strength + other.ranged_strength,
            magic_strength=self.magic_strength + other.magic_strength,
        )
