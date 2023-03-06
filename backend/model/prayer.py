from enum import Enum
from dataclasses import dataclass


@dataclass()
class PrayerMultiplier:
    attack: float = 0
    strength: float = 0

    ranged: float = 0
    ranged_strength: float = 0

    magic: float = 0

    @staticmethod
    def sum_prayers(prayers):
        att = 0
        stre = 0
        rng = 0
        rngstr = 0
        mag = 0
        for prayer in prayers:
            att += prayer.value.attack
            stre += prayer.value.strength
            rng += prayer.value.ranged
            rngstr += prayer.value.ranged_strength
            mag += prayer.value.magic

        return PrayerMultiplier(max(att, 1), max(stre, 1), max(rng, 1), max(rngstr, 1), max(mag, 1))


class Prayer(Enum):
    PIETY = PrayerMultiplier(attack=1.20, strength=1.23)
    CHIVALRY = PrayerMultiplier(attack=1.15, strength=1.18)
    RIGOUR = PrayerMultiplier(ranged=1.20, ranged_strength=1.23)
    EAGLE_EYE = PrayerMultiplier(ranged=1.15, ranged_strength=1.15)
    AUGURY = PrayerMultiplier(magic=1.25)
