import json
import unittest
from pathlib import Path
from unittest.mock import Mock

from damage_sim.damage_sim_graph import DamageSimGraph
from damage_sim.damage_sim_runner import DamageSimRunner
from input_setup.input_setup_converter import InputSetupConverter
from model.input_setup.input_setup import InputSetup
from model.npc.npc_ids import VARDORVIS

TEST_RESOURCE_FOLDER = Path(__file__).parent.parent / "tests/resources"
TEST_ITERATIONS = 100
NPC_HITPOINTS = 10_000


class TestDamageSimRunner(unittest.TestCase):
    input_setups: dict
    spec_input_setups: dict

    @classmethod
    def setUpClass(cls):
        with open(TEST_RESOURCE_FOLDER / "input_setups.json") as f:
            TestDamageSimRunner.input_setups = json.load(f)

        with open(TEST_RESOURCE_FOLDER / "spec_input_setups.json") as f:
            TestDamageSimRunner.spec_input_setups = json.load(f)

    @staticmethod
    def print_sim_dps_diff_message(expected_dps, sim_dps, setup_name):
        dps_diff = abs(expected_dps - sim_dps)
        dps_diff_percent = (dps_diff / expected_dps) * 100

        print("dps diff: " + "{:.2f}".format(dps_diff_percent) + "%: " + setup_name)

    @staticmethod
    def initialise_input_setup(input_setup: InputSetup, limit_defence=False):
        input_setup.global_settings.iterations = TEST_ITERATIONS
        input_setup.global_settings.is_detailed_run = False
        input_setup.global_settings.npc.base_combat_stats.hitpoints = NPC_HITPOINTS
        if limit_defence:
            input_setup.global_settings.npc.min_defence = input_setup.global_settings.npc.base_combat_stats.defence
        for weapon in input_setup.input_gear_setups[0].all_weapons:
            weapon.set_npc(input_setup.global_settings.npc)
            if input_setup.global_settings.npc.id in VARDORVIS:
                weapon.is_pre_attack = False

    def test_input_setup_run_single_gear_setup(self):
        print("\nTesting setup sim dps:")
        for setup_name in TestDamageSimRunner.input_setups:
            with self.subTest():
                input_setup = InputSetupConverter.get_input_setup(TestDamageSimRunner.input_setups[setup_name])

                TestDamageSimRunner.initialise_input_setup(input_setup)

                total_damage_sim_data, _, _ = DamageSimRunner.run_single_gear_setup(input_setup.global_settings,
                                                                                    input_setup.input_gear_setups[0])

                dps_sum = 0
                for dps in total_damage_sim_data.gear_dps:
                    dps_sum += dps[0]
                sim_dps_average = dps_sum / TEST_ITERATIONS
                self.assertAlmostEqual(TestDamageSimRunner.input_setups[setup_name]["expectedDps"],
                                       sim_dps_average, delta=1, msg=setup_name)

                TestDamageSimRunner.print_sim_dps_diff_message(
                    TestDamageSimRunner.input_setups[setup_name]["expectedDps"],
                    sim_dps_average,
                    setup_name
                )

    def test_input_setup_run_dps_calc(self):
        for setup_name in TestDamageSimRunner.input_setups:
            with self.subTest():
                input_setup = InputSetupConverter.get_input_setup(TestDamageSimRunner.input_setups[setup_name])

                TestDamageSimRunner.initialise_input_setup(input_setup)

                dps_calc_results = DamageSimRunner.run_dps_calc(input_setup)

                actual_dps = round(dps_calc_results.results[0].theoretical_dps[0], 8)
                self.assertEqual(TestDamageSimRunner.input_setups[setup_name]["expectedDps"],
                                 actual_dps, msg=setup_name)

    def test_spec_input_setup_run_single_gear_setup(self):
        print("\nTesting spec setup sim dps:")
        for setup_name in TestDamageSimRunner.spec_input_setups:
            with self.subTest():
                input_setup = InputSetupConverter.get_input_setup(TestDamageSimRunner.spec_input_setups[setup_name])

                TestDamageSimRunner.initialise_input_setup(input_setup, limit_defence=True)
                input_setup.input_gear_setups[0].main_weapon.gear_setup.is_special_attack = True

                total_damage_sim_data, _, _ = DamageSimRunner.run_single_gear_setup(input_setup.global_settings,
                                                                                    input_setup.input_gear_setups[0])

                dps_sum = 0
                for dps in total_damage_sim_data.gear_dps:
                    dps_sum += dps[0]
                sim_dps_average = dps_sum / TEST_ITERATIONS
                self.assertAlmostEqual(TestDamageSimRunner.spec_input_setups[setup_name]["expectedDps"],
                                       sim_dps_average, delta=1, msg=setup_name)

                TestDamageSimRunner.print_sim_dps_diff_message(
                    TestDamageSimRunner.spec_input_setups[setup_name]["expectedDps"],
                    sim_dps_average,
                    setup_name
                )

    def test_run(self):
        damage_sim_runner = DamageSimRunner(Mock())
        input_setup = InputSetupConverter.get_input_setup(TestDamageSimRunner.input_setups["Vorkath max dhcb"])
        damage_sim_results = damage_sim_runner.run(input_setup)

        self.assertIsNotNone(damage_sim_results.results)
        self.assertIsNotNone(damage_sim_results.global_settings_label)


if __name__ == '__main__':
    unittest.main()
