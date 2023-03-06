from model.gear_setup import GearSetup
from model.input_setup.gear_setup_settings import GearSetupSettings
from model.npc.npc_stats import NpcStats
from weapon import Weapon
from weapons.custom_weapons import CUSTOM_WEAPONS


class WeaponLoader:

    @staticmethod
    def load_weapon(weapon_name, gear_setup: GearSetup, gear_setup_settings: GearSetupSettings,
                    npc: NpcStats, raid_level) -> Weapon:
        if weapon_name in CUSTOM_WEAPONS:
            weapon = CUSTOM_WEAPONS[weapon_name](gear_setup, gear_setup_settings.combat_stats, npc, raid_level)
        else:
            weapon = Weapon(gear_setup, gear_setup_settings.combat_stats, npc, raid_level)

        return weapon
