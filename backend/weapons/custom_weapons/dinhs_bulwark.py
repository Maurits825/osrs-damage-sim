from model.gear_setup import GearSetup
from model.npc.combat_stats import CombatStats
from model.npc.npc_stats import NpcStats
from weapons.weapon import Weapon
from wiki_data.wiki_data import WikiData


class DinhsBulwark(Weapon):
    def __init__(self, gear_setup: GearSetup, combat_stats: CombatStats, npc: NpcStats, raid_level):
        super().__init__(gear_setup, combat_stats, npc, raid_level)

        self.gear_setup.gear_stats.melee_strength += self.get_strength_buff()

    def get_strength_buff(self):
        defence_sum = 0
        for defence_stat in ["dstab", "dslash", "dcrush", "drange"]:
            defence_sum += self.get_defence_stat_sum(defence_stat)

        return (((defence_sum / 4) - 200) / 3) - 38

    def get_defence_stat_sum(self, key_name):
        defence_sum = 0
        for gear_id in self.gear_setup.equipped_gear.ids:
            defence_sum += WikiData.get_item(gear_id).get(key_name, 0)
        return defence_sum
