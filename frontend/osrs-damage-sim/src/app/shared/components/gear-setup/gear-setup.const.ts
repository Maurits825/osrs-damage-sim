import { GearSetup } from 'src/app/model/damage-sim/input-setup.model';
import { GearSlot } from 'src/app/model/osrs/gear-slot.enum';

export const SPECIAL_BOLTS = [9242, 21944, 9243, 21946];
export const DRAGON_DARTS_ID = 11230;
export const BLOWPIPE_ID = 12926;
export const UNARMED_EQUIVALENT_ID = 3689;
export const AUTOCAST_STLYE = 'Spell (Magic/Autocast)';
export const WILDY_WEAPONS = [22547, 27652, 22552, 27785, 27662, 27676, 22542, 27657];

export const DEFAULT_GEAR_SETUP: GearSetup = {
  setupName: null,
  presetName: null,
  gear: {
    [GearSlot.Head]: null,
    [GearSlot.Cape]: null,
    [GearSlot.Neck]: null,
    [GearSlot.Weapon]: null,
    [GearSlot.Body]: null,
    [GearSlot.Shield]: null,
    [GearSlot.Legs]: null,
    [GearSlot.Hands]: null,
    [GearSlot.Feet]: null,
    [GearSlot.Ring]: null,
    [GearSlot.Ammo]: null,
  },
  blowpipeDarts: null,
  attackStyle: null,
  spell: null,
  isSpecial: false,
  prayers: new Set(),
  conditions: [],
  statDrain: [],
  isOnSlayerTask: true,
  isInWilderness: true,
  currentHp: 1,
  miningLvl: 99,
  isKandarinDiary: true,
};
