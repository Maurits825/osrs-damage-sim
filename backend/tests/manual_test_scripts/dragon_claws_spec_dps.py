import json
from pathlib import Path

from damage_sim.damage_sim import DamageSim
from input_setup.input_setup_converter import InputSetupConverter

TEST_RESOURCE_FOLDER = Path(__file__).parent.parent.parent / "tests/resources"


class DragonClawsDps:
    def sim_dps(self):
        with open(TEST_RESOURCE_FOLDER / "spec_input_setups.json") as f:
            input_setups = json.load(f)

        input_setup = InputSetupConverter.get_input_setup(input_setups["Ba-ba 300 max d claws spec"])
        input_setup.input_gear_setups[0].main_weapon.npc.base_combat_stats.hitpoints = 100_000_000
        damage_sim = DamageSim(input_setup.input_gear_setups[0], input_setup.global_settings)
        dmg_sim_data = damage_sim.run_damage_sim()

        print("Sim dps: " + str(dmg_sim_data.gear_dps[0]))
        print("Theoretical dps: " + str(input_setup.input_gear_setups[0].main_weapon.get_dps()))


if __name__ == "__main__":
    claws = DragonClawsDps()
    claws.sim_dps()
