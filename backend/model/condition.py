from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ConditionVariables(Enum):
    NPC_HITPOINTS = 1,
    DMG_DEALT = 2,
    ATTACK_COUNT = 3,


class ConditionComparison(Enum):
    AND = 1,
    OR = 2,
    EQUAL = 3,
    GRT_THAN = 4,
    LESS_THAN = 5,
    GRT_EQ_THAN = 6,
    LESS_EQ_THAN = 7,


@dataclass()
class Condition:
    variable: ConditionVariables
    comparison: ConditionComparison
    value: int
    nextComparison: ConditionComparison | None
