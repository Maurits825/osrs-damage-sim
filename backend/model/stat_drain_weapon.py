from model.npc.npc_stats import NpcStats
from model.stat_drain_type import StatDrainType


class StatDrainWeapon:
    stat_drain_type: StatDrainType

    @staticmethod
    def drain_stats(npc: NpcStats, value):
        pass
