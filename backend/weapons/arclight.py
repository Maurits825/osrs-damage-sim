import math

from model.npc.npc_stats import NpcStats
from model.stat_drain_type import StatDrainType
from model.stat_drain_weapon import StatDrainWeapon
from weapon import Weapon


class Arclight(Weapon, StatDrainWeapon):
    stat_drain_type = StatDrainType.HITS

    def roll_hit(self) -> bool:
        roll_hit = super().roll_hit()

        if roll_hit and self.gear_setup.is_special_attack:
            Arclight.drain_stats(self.npc, None)

        return roll_hit

    @staticmethod
    def drain_stats(npc: NpcStats, _):
        if npc.is_demon:
            Arclight.drain_stats_percent(npc, 10)
        else:
            Arclight.drain_stats_percent(npc, 5)

    @staticmethod
    def drain_stats_percent(npc: NpcStats, percent):
        npc.combat_stats.defence = max(
            npc.min_defence,
            npc.combat_stats.defence - (math.floor(npc.base_combat_stats.defence * (percent / 100)) + 1)
        )
