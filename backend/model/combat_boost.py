class DpsBoost:
    def __init__(self):
        self.attack_boost = [1]
        self.strength_boost = [1]


class CombatBoost:
    def __init__(self):
        self.melee: DpsBoost = DpsBoost()
        self.ranged: DpsBoost = DpsBoost()
        self.magic: DpsBoost = DpsBoost()
