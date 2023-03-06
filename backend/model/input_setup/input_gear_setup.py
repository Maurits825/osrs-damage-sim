from dataclasses import dataclass, field

from model.input_setup.gear_setup_settings import GearSetupSettings
from weapon import Weapon


@dataclass()
class InputGearSetup:
    gear_setup_settings: GearSetupSettings
    main_weapon: Weapon
    fill_weapons: list[Weapon]

    all_weapons: list[Weapon] = field(init=False)

    def __post_init__(self):
        self.all_weapons = [self.main_weapon, *self.fill_weapons]
