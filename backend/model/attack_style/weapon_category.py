from enum import Enum

from model.attack_style.attack_style import AttackStyle
from model.attack_style.attack_type import AttackType
from model.attack_style.combat_style import CombatStyle


class WeaponCategory(Enum):
    TWO_HANDED_SWORD = [
        AttackStyle("Chop (Slash/Accurate)", AttackType.SLASH, CombatStyle.ACCURATE),
        AttackStyle("Slash (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Smash (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Slash/Defensive)", AttackType.SLASH, CombatStyle.DEFENSIVE)
    ]
    AXE = [
        AttackStyle("Chop (Slash/Accurate)", AttackType.SLASH, CombatStyle.ACCURATE),
        AttackStyle("Hack (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Smash (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Slash/Defensive)", AttackType.SLASH, CombatStyle.DEFENSIVE)
    ]
    BANNER = [
        AttackStyle("Lunge (Stab/Accurate)", AttackType.STAB, CombatStyle.ACCURATE),
        AttackStyle("Swipe (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Pound (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Stab/Defensive)", AttackType.STAB, CombatStyle.DEFENSIVE)
    ]
    BLADED_STAFF = [
        AttackStyle("Jab (Stab/Accurate)", AttackType.STAB, CombatStyle.ACCURATE),
        AttackStyle("Swipe (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Fend (Crush/Defensive)", AttackType.CRUSH, CombatStyle.DEFENSIVE),
        AttackStyle("Spell (Magic/Autocast)", AttackType.MAGIC, CombatStyle.AUTOCAST)
    ]
    BLUDGEON = [
        AttackStyle("Pound (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Pummel (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Smash (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE)
    ]
    BLUNT = [
        AttackStyle("Pound (Crush/Accurate)", AttackType.CRUSH, CombatStyle.ACCURATE),
        AttackStyle("Pummel (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Crush/Defensive)", AttackType.CRUSH, CombatStyle.DEFENSIVE)
    ]
    BOW = [
        AttackStyle("Accurate (Ranged/Accurate)", AttackType.RANGED, CombatStyle.ACCURATE),
        AttackStyle("Rapid (Ranged/Rapid)", AttackType.RANGED, CombatStyle.RAPID),
        AttackStyle("Longrange (Ranged/Longrange)", AttackType.RANGED, CombatStyle.LONGRANGE)
    ]
    BULWARK = [
        AttackStyle("Pummel (Crush/Accurate)", AttackType.CRUSH, CombatStyle.ACCURATE)
    ]
    CHINCHOMPAS = [
        AttackStyle("Short fuse (Ranged/Accurate)", AttackType.RANGED, CombatStyle.ACCURATE),
        AttackStyle("Medium fuse (Ranged/Rapid)", AttackType.RANGED, CombatStyle.RAPID),
        AttackStyle("Long fuse (Ranged/Longrange)", AttackType.RANGED, CombatStyle.LONGRANGE)
    ]
    CLAW = [
        AttackStyle("Chop (Slash/Accurate)", AttackType.SLASH, CombatStyle.ACCURATE),
        AttackStyle("Slash (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Lunge (Stab/Controlled)", AttackType.STAB, CombatStyle.CONTROLLED),
        AttackStyle("Block (Slash/Defensive)", AttackType.SLASH, CombatStyle.DEFENSIVE)
    ]
    CROSSBOW = [
        AttackStyle("Accurate (Ranged/Accurate)", AttackType.RANGED, CombatStyle.ACCURATE),
        AttackStyle("Rapid (Ranged/Rapid)", AttackType.RANGED, CombatStyle.RAPID),
        AttackStyle("Longrange (Ranged/Longrange)", AttackType.RANGED, CombatStyle.LONGRANGE)
    ]
    PARTISAN = [
        AttackStyle("Stab (Stab/Accurate)", AttackType.STAB, CombatStyle.ACCURATE),
        AttackStyle("Lunge (Stab/Aggressive)", AttackType.STAB, CombatStyle.ACCURATE),
        AttackStyle("Pound (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.ACCURATE),
        AttackStyle("Block (Stab/Defensive)", AttackType.STAB, CombatStyle.ACCURATE)
    ]
    PICKAXE = [
        AttackStyle("Spike (Stab/Accurate)", AttackType.STAB, CombatStyle.ACCURATE),
        AttackStyle("Impale (Stab/Aggressive)", AttackType.STAB, CombatStyle.AGGRESSIVE),
        AttackStyle("Smash (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Stab/Defensive)", AttackType.STAB, CombatStyle.DEFENSIVE)
    ]
    POLEARM = [
        AttackStyle("Jab (Stab/Controlled)", AttackType.STAB, CombatStyle.CONTROLLED),
        AttackStyle("Swipe (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Fend (Stab/Defensive)", AttackType.STAB, CombatStyle.DEFENSIVE)
    ]
    POLESTAFF = [
        AttackStyle("Bash (Crush/Accurate)", AttackType.CRUSH, CombatStyle.ACCURATE),
        AttackStyle("Pound (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Crush/Defensive)", AttackType.CRUSH, CombatStyle.DEFENSIVE)
    ]
    POWERED_STAFF = [
        AttackStyle("Accurate (Magic/Accurate)", AttackType.MAGIC, CombatStyle.ACCURATE),
        AttackStyle("Accurate (Magic/Accurate)", AttackType.MAGIC, CombatStyle.ACCURATE),
        AttackStyle("Longrange (Magic/Longrange)", AttackType.MAGIC, CombatStyle.LONGRANGE)
    ]
    SALAMANDER = [
        AttackStyle("Scorch (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Flare (Ranged/Accurate)", AttackType.RANGED, CombatStyle.ACCURATE),
        AttackStyle("Blaze (Magic/Defensive)", AttackType.MAGIC, CombatStyle.DEFENSIVE)
    ]
    SCYTHE = [
        AttackStyle("Reap (Slash/Accurate)", AttackType.SLASH, CombatStyle.ACCURATE),
        AttackStyle("Chop (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Jab (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Slash/Defensive)", AttackType.SLASH, CombatStyle.DEFENSIVE)
    ]
    SLASH_SWORD = [
        AttackStyle("Chop (Slash/Accurate)", AttackType.SLASH, CombatStyle.ACCURATE),
        AttackStyle("Slash (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Lunge (Stab/Controlled)", AttackType.STAB, CombatStyle.CONTROLLED),
        AttackStyle("Block (Slash/Defensive)", AttackType.SLASH, CombatStyle.DEFENSIVE)
    ]
    SPEAR = [
        AttackStyle("Lunge (Stab/Controlled)", AttackType.STAB, CombatStyle.CONTROLLED),
        AttackStyle("Swipe (Slash/Controlled)", AttackType.SLASH, CombatStyle.CONTROLLED),
        AttackStyle("Pound (Crush/Controlled)", AttackType.CRUSH, CombatStyle.CONTROLLED),
        AttackStyle("Block (Stab/Defensive)", AttackType.STAB, CombatStyle.DEFENSIVE)
    ]
    SPIKED = [
        AttackStyle("Pound (Crush/Accurate)", AttackType.CRUSH, CombatStyle.ACCURATE),
        AttackStyle("Pummel (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Spike (Stab/Controlled)", AttackType.STAB, CombatStyle.CONTROLLED),
        AttackStyle("Block (Crush/Defensive)", AttackType.CRUSH, CombatStyle.DEFENSIVE)
    ]
    STAB_SWORD = [
        AttackStyle("Stab (Stab/Accurate)", AttackType.STAB, CombatStyle.ACCURATE),
        AttackStyle("Lunge (Stab/Aggressive)", AttackType.STAB, CombatStyle.AGGRESSIVE),
        AttackStyle("Slash (Slash/Aggressive)", AttackType.SLASH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Stab/Defensive)", AttackType.STAB, CombatStyle.DEFENSIVE)
    ]
    STAFF = [
        AttackStyle("Bash (Crush/Accurate)", AttackType.CRUSH, CombatStyle.ACCURATE),
        AttackStyle("Pound (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Focus (Crush/Defensive)", AttackType.CRUSH, CombatStyle.DEFENSIVE),
        AttackStyle("Spell (Magic/Autocast)", AttackType.MAGIC, CombatStyle.AUTOCAST)
    ]
    THROWN = [
        AttackStyle("Accurate (Ranged/Accurate)", AttackType.RANGED, CombatStyle.ACCURATE),
        AttackStyle("Rapid (Ranged/Rapid)", AttackType.RANGED, CombatStyle.RAPID),
        AttackStyle("Longrange (Ranged/Longrange)", AttackType.RANGED, CombatStyle.LONGRANGE)
    ]
    UNARMED = [
        AttackStyle("Punch (Crush/Accurate)", AttackType.CRUSH, CombatStyle.ACCURATE),
        AttackStyle("Kick (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
        AttackStyle("Block (Crush/Defensive)", AttackType.CRUSH, CombatStyle.DEFENSIVE)
    ]
    WHIP = [
        AttackStyle("Flick (Slash/Accurate)", AttackType.SLASH, CombatStyle.ACCURATE),
        AttackStyle("Lash (Slash/Controlled)", AttackType.SLASH, CombatStyle.CONTROLLED),
        AttackStyle("Deflect (Slash/Defensive)", AttackType.SLASH, CombatStyle.DEFENSIVE)
    ]
    GUN = [
        AttackStyle("Kick (Crush/Aggressive)", AttackType.CRUSH, CombatStyle.AGGRESSIVE),
    ]
