from dataclasses import dataclass


@dataclass()
class CombatStats:
    hitpoints: int
    attack: int
    strength: int
    defence: int
    magic: int
    ranged: int

    def set_stats(self, combat_stats):
        self.hitpoints = combat_stats.hitpoints
        self.attack = combat_stats.attack
        self.strength = combat_stats.strength
        self.defence = combat_stats.defence
        self.magic = combat_stats.magic
        self.ranged = combat_stats.ranged

    def merge_stats(self, combat_stats):
        self.hitpoints = max(self.hitpoints, combat_stats.hitpoints)
        self.attack = max(self.attack, combat_stats.attack)
        self.strength = max(self.strength, combat_stats.strength)
        self.defence = max(self.defence, combat_stats.defence)
        self.magic = max(self.magic, combat_stats.magic)
        self.ranged = max(self.ranged, combat_stats.ranged)
