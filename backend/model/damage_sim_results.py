from dataclasses import dataclass

from model.graph import GraphType
from model.sim_stats import TimeSimStats, SimStats


@dataclass()
class GearSetupDpsStats:
    theoretical_dps: list[float]
    max_hit: list[int]
    accuracy: list[float]


@dataclass()
class SingleDamageSimData:
    ticks_to_kill: int
    gear_total_dmg: list[int]
    gear_attack_count: list[int]
    gear_dps: list[float]


@dataclass()
class TotalDamageSimData:
    ticks_to_kill: list[int]
    gear_total_dmg: list[list[int]]
    gear_attack_count: list[list[int]]
    gear_dps: list[list[float]]


@dataclass()
class InputGearSetupLabels:
    input_gear_setup_label: str
    gear_setup_settings_label: str
    all_weapon_labels: list[str]


@dataclass()
class DamageSimResults:
    labels: list[InputGearSetupLabels]

    ttk_stats: list[TimeSimStats]
    total_damage_stats: list[list[SimStats]]
    attack_count_stats: list[list[SimStats]]
    sim_dps_stats: list[list[SimStats]]
    cumulative_chances: list[list[float]]

    theoretical_dps: list[list[float]]
    max_hit: list[list[int]]
    accuracy: list[list[float]]

    graphs: dict[GraphType, str]
