from dataclasses import dataclass

from model.boost import BoostType
from model.input_setup.stat_drain import StatDrain
from model.npc.combat_stats import CombatStats


@dataclass()
class GearSetupSettings:
    combat_stats: CombatStats
    boosts: list[BoostType]
    stat_drains: list[StatDrain]
