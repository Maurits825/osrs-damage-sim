from dataclasses import dataclass

from model.npc.npc_stats import NpcStats


@dataclass()
class GlobalSettings:
    npc: NpcStats

    raid_level: int
    path_level: int

    team_size: int
    iterations: int
