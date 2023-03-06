from dataclasses import dataclass

from model.input_setup.global_settings import GlobalSettings
from model.input_setup.input_gear_setup import InputGearSetup


@dataclass()
class InputSetup:
    global_settings: GlobalSettings
    input_gear_setups: list[InputGearSetup]
