import json
import unittest
from pathlib import Path

from damage_sim.damage_sim import DamageSim
from input_setup.input_setup_converter import InputSetupConverter

TEST_RESOURCE_FOLDER = Path(__file__).parent.parent / "tests/resources"


class TestWeaponDps(unittest.TestCase):
    input_setups: dict
    spec_input_setups: dict

    @classmethod
    def setUpClass(cls):
        with open(TEST_RESOURCE_FOLDER / "input_setups.json") as f:
            TestWeaponDps.input_setups = json.load(f)

        with open(TEST_RESOURCE_FOLDER / "spec_input_setups.json") as f:
            TestWeaponDps.spec_input_setups = json.load(f)

    def test_input_setups_dps(self):
        print("Testing setup dps:")
        for setup_name in TestWeaponDps.input_setups:
            with self.subTest():
                input_setup = InputSetupConverter.get_input_setup(TestWeaponDps.input_setups[setup_name])
                damage_sim = DamageSim(input_setup.global_settings.npc, input_setup.input_gear_setups[0])
                gear_setup_dps_stats = damage_sim.get_weapon_dps_stats()
                dps = round(gear_setup_dps_stats.theoretical_dps[0], 8)

                print(setup_name + " - " + str(dps))
                self.assertEqual(TestWeaponDps.input_setups[setup_name]["expectedDps"], dps, setup_name)

    def test_special_attack_input_setups_dps(self):
        print("Testing spec setup dps:")
        for setup_name in TestWeaponDps.spec_input_setups:
            with self.subTest():
                input_setup = InputSetupConverter.get_input_setup(TestWeaponDps.spec_input_setups[setup_name])
                damage_sim = DamageSim(input_setup.global_settings.npc, input_setup.input_gear_setups[0])
                gear_setup_dps_stats = damage_sim.get_weapon_dps_stats()
                dps = round(gear_setup_dps_stats.theoretical_dps[1], 8)

                print(setup_name + " - " + str(dps))
                self.assertEqual(TestWeaponDps.spec_input_setups[setup_name]["expectedDps"], dps, setup_name)


if __name__ == '__main__':
    unittest.main()
