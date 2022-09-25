from dataclasses import dataclass

from model.aggressive_stats import AggressiveStats
from model.combat_stats import CombatStats
from model.defensive_stats import DefensiveStats


@dataclass()
class NpcStats:
    name: str

    combat_stats: CombatStats
    aggressive_stats: AggressiveStats
    defensive_stats: DefensiveStats

    min_defence: int = 0

    def drain_defence(self, amount):
        self.combat_stats.defence = max(self.min_defence, self.combat_stats.defence - amount)