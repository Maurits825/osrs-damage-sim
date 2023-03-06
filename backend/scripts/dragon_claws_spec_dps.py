import json
from pathlib import Path

from damage_sim.damage_sim import DamageSim
from input_setup.input_setup_converter import InputSetupConverter

TEST_RESOURCE_FOLDER = Path(__file__).parent.parent / "tests/resources"


class DragonClawsDps:
    def sim_dps(self):
        with open(TEST_RESOURCE_FOLDER / "input_setups.json") as f:
            input_setups = json.load(f)

        input_setup = InputSetupConverter.get_input_setup(input_setups["Ba-ba 300 max d claws spec"])
        input_setup.npc.combat_stats.hitpoints = 10_000_000
        damage_sim = DamageSim(input_setup.npc, input_setup.all_weapons_setups[0])
        dmg_sim_data = damage_sim.run()

        print("Sim dps: " + str(dmg_sim_data.gear_dps[0]))
        print("Theoretical dps: " + str(input_setup.all_weapons_setups[0][0].get_dps()))


if __name__ == "__main__":
    claws = DragonClawsDps()
    claws.sim_dps()
