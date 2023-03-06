from dataclasses import dataclass


@dataclass()
class TimeSimStats:
    average: str
    maximum: str
    minimum: str
    most_frequent: str

    chance_to_kill: list[str]


@dataclass()
class SimStats:
    average: float
    maximum: int
    minimum: int
    most_frequent: int

    chance_to_kill: list
