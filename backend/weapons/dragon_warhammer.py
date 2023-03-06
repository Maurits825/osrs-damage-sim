import math

from model.npc.npc_stats import NpcStats
from model.stat_drain_type import StatDrainType
from model.stat_drain_weapon import StatDrainWeapon
from weapon import Weapon


class DragonWarhammer(Weapon, StatDrainWeapon):
    stat_drain_type = StatDrainType.HITS

    def get_max_hit(self):
        if self.gear_setup.is_special_attack:
            return math.floor(super().get_max_hit() * 1.5)
        else:
            return super().get_max_hit()

    def roll_damage(self) -> int:
        damage = super().roll_damage()
        if self.gear_setup.is_special_attack:
            DragonWarhammer.drain_stats(self.npc, damage)
        return damage

    @staticmethod
    def drain_stats(npc: NpcStats, damage):
        if damage != 0:
            DragonWarhammer.drain_defence_percent(npc, 30)
        elif "Tekton" in npc.name:  # TODO test
            DragonWarhammer.drain_defence_percent(npc, 5)

    @staticmethod
    def drain_defence_percent(npc: NpcStats, percent):
        npc.combat_stats.defence = max(
            npc.min_defence, npc.combat_stats.defence - math.floor(npc.combat_stats.defence * (percent / 100))
        )
