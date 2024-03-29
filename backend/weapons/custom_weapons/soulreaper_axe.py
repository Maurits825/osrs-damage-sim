from model.damage_sim_results.special_proc import SpecialProc
from model.gear_setup import GearSetup
from model.hitsplat import Hitsplat
from model.input_setup.gear_setup_settings import GearSetupSettings
from model.npc.npc_stats import NpcStats
from model.prayer import PrayerMultiplier
from weapons.weapon import Weapon

MAX_MIGHTY_STACK = 5
MIGHTY_STACK_MULTIPLIER = 0.06


class SoulreaperAxe(Weapon):
    def __init__(self, gear_setup: GearSetup, gear_setup_settings: GearSetupSettings, npc: NpcStats, player,
                 raid_level):
        super().__init__(gear_setup, gear_setup_settings, npc, player, raid_level)

        self.reset()

    def attack(self) -> Hitsplat:
        if self.player.is_weapon_switched:
            self.reset()

        hitsplat = super().attack()

        if self.mighty_stack < MAX_MIGHTY_STACK:
            self.mighty_stack += 1
            hitsplat.special_procs.append(SpecialProc.MIGHTY_STACK_GAIN)
            self.prayer_multiplier.strength += MIGHTY_STACK_MULTIPLIER

            self.max_hit = self.get_max_hit()

        return hitsplat

    # TODO special attack... uses stacks not spec energy

    def get_dps_max_hit(self):
        self.prayer_multiplier.strength += MAX_MIGHTY_STACK * MIGHTY_STACK_MULTIPLIER

        return self.get_max_hit()

    def reset(self):
        self.mighty_stack = 0
        self.prayer_multiplier = PrayerMultiplier.sum_prayers(self.gear_setup.prayers)
        self.max_hit = self.get_max_hit()
