import math
from copy import deepcopy
from dataclasses import dataclass
from aenum import Enum, NoAlias

from model.npc.combat_stats import CombatStats


@dataclass()
class BoostAmount:
    percent: float
    base: int


@dataclass()
class BoostStat:
    attack: BoostAmount = BoostAmount(0, 0)
    strength: BoostAmount = BoostAmount(0, 0)
    defence: BoostAmount = BoostAmount(0, 0)
    ranged: BoostAmount = BoostAmount(0, 0)
    magic: BoostAmount = BoostAmount(0, 0)


class BoostType(Enum):
    _settings_ = NoAlias

    ATTACK = BoostStat(attack=BoostAmount(10, 3))
    SUPER_ATTACK = BoostStat(attack=BoostAmount(15, 5))
    DIVINE_SUPER_ATTACK = BoostStat(attack=BoostAmount(15, 5))
    STRENGTH = BoostStat(strength=BoostAmount(10, 3))
    SUPER_STRENGTH = BoostStat(strength=BoostAmount(15, 5))
    DIVINE_SUPER_STRENGTH = BoostStat(strength=BoostAmount(15, 5))
    COMBAT = BoostStat(attack=BoostAmount(10, 3), strength=BoostAmount(10, 3))
    SUPER_COMBAT = BoostStat(attack=BoostAmount(15, 5), strength=BoostAmount(15, 5), defence=BoostAmount(15, 5))
    DIVINE_SUPER_COMBAT = BoostStat(attack=BoostAmount(15, 5), strength=BoostAmount(15, 5), defence=BoostAmount(15, 5))
    ZAMORAK_BREW = BoostStat(attack=BoostAmount(20, 2), strength=BoostAmount(12, 2))
    OVERLOAD_PLUS = BoostStat(attack=BoostAmount(16, 6), strength=BoostAmount(16, 6), defence=BoostAmount(16, 6),
                              ranged=BoostAmount(16, 6), magic=BoostAmount(16, 6))
    SMELLING_SALTS = BoostStat(attack=BoostAmount(16, 11), strength=BoostAmount(16, 11), defence=BoostAmount(16, 11),
                               ranged=BoostAmount(16, 11), magic=BoostAmount(16, 11))
    MAGIC = BoostStat(magic=BoostAmount(0, 4))
    DIVINE_MAGIC = BoostStat(magic=BoostAmount(0, 4))
    ANCIENT_BREW = BoostStat(magic=BoostAmount(5, 2))
    FORGOTTEN_BREW = BoostStat(magic=BoostAmount(8, 3))
    IMBUED_HEART = BoostStat(magic=BoostAmount(10, 1))
    SATURATED_HEART = BoostStat(magic=BoostAmount(10, 4))
    RANGING = BoostStat(ranged=BoostAmount(10, 4))
    DIVINE_RANGING = BoostStat(ranged=BoostAmount(10, 4))
    LIQUID_ADRENALINE = BoostStat()


class Boost:
    @staticmethod
    def apply_boost(boost_type: BoostType, combat_stats: CombatStats):
        combat_stats.attack += (math.floor(combat_stats.attack * (boost_type.value.attack.percent / 100)) +
                                boost_type.value.attack.base)
        combat_stats.strength += (math.floor(combat_stats.strength * (boost_type.value.strength.percent / 100)) +
                                  boost_type.value.strength.base)
        combat_stats.defence += (math.floor(combat_stats.defence * (boost_type.value.defence.percent / 100)) +
                                 boost_type.value.defence.base)
        combat_stats.ranged += (math.floor(combat_stats.ranged * (boost_type.value.ranged.percent / 100)) +
                                boost_type.value.ranged.base)
        combat_stats.magic += (math.floor(combat_stats.magic * (boost_type.value.magic.percent / 100)) +
                               boost_type.value.magic.base)

    @staticmethod
    def apply_boosts(initial_combat_stats: CombatStats, boosts: list[BoostType]):
        boosted_combat_stats = deepcopy(initial_combat_stats)
        for boost in boosts:
            combat_stats = deepcopy(initial_combat_stats)
            Boost.apply_boost(boost, combat_stats)
            boosted_combat_stats.merge_stats(combat_stats)

        initial_combat_stats.merge_stats(boosted_combat_stats)
