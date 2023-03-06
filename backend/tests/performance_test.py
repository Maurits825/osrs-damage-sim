import json
from pathlib import Path

from damage_sim.damage_sim_runner import DamageSimRunner
from input_setup.input_setup_converter import InputSetupConverter

TEST_RESOURCE_FOLDER = Path(__file__).parent.parent / "tests/resources"


class PerformanceTest:
    def __init__(self):
        with open(TEST_RESOURCE_FOLDER / "performance_test_input_setups.json") as f:
            self.input_setups = json.load(f)

    def run(self):
        damage_sim_runner = DamageSimRunner()
        input_setup = InputSetupConverter.get_input_setup(self.input_setups["Performance test setup 1"])
        _ = damage_sim_runner.run(input_setup)


if __name__ == '__main__':
    performance_test = PerformanceTest()
    performance_test.run()
