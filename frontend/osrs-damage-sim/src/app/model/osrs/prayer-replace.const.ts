import { Prayer, ReplacePrayer } from './prayer.model';

export const attackPrayers: Set<Prayer> = new Set([
  'clarity_of_thought',
  'sharp_eye',
  'mystic_will',
  'improved_reflexes',
  'hawk_eye',
  'mystic_lore',
  'incredible_reflexes',
  'eagle_eye',
  'mystic_might',
  'chivalry',
  'piety',
  'rigour',
  'augury',
]);

export const strengthPrayers: Set<Prayer> = new Set([
  'burst_of_strength',
  'sharp_eye',
  'mystic_will',
  'superhuman_strength',
  'hawk_eye',
  'mystic_lore',
  'ultimate_strength',
  'eagle_eye',
  'mystic_might',
  'chivalry',
  'piety',
  'rigour',
  'augury',
]);

export const defencePrayers: Set<Prayer> = new Set([
  'thick_skin',
  'rock_skin',
  'steel_skin',
  'chivalry',
  'piety',
  'rigour',
  'augury',
]);

export const overheadPrayers: Set<Prayer> = new Set([
  'protect_from_magic',
  'protect_from_missiles',
  'protect_from_melee',
  'retribution',
  'redemption',
  'smite',
]);

export const replacePrayers: ReplacePrayer = {
  thick_skin: defencePrayers,
  burst_of_strength: strengthPrayers,
  clarity_of_thought: attackPrayers,
  sharp_eye: new Set([...attackPrayers, ...strengthPrayers]),
  mystic_will: new Set([...attackPrayers, ...strengthPrayers]),
  rock_skin: defencePrayers,
  superhuman_strength: strengthPrayers,
  improved_reflexes: attackPrayers,
  rapid_heal: null,
  rapid_restore: null,
  protect_item: null,
  hawk_eye: new Set([...attackPrayers, ...strengthPrayers]),
  mystic_lore: new Set([...attackPrayers, ...strengthPrayers]),
  steel_skin: defencePrayers,
  ultimate_strength: strengthPrayers,
  incredible_reflexes: attackPrayers,
  protect_from_magic: overheadPrayers,
  protect_from_missiles: overheadPrayers,
  protect_from_melee: overheadPrayers,
  eagle_eye: new Set([...attackPrayers, ...strengthPrayers]),
  mystic_might: new Set([...attackPrayers, ...strengthPrayers]),
  retribution: overheadPrayers,
  redemption: overheadPrayers,
  smite: overheadPrayers,
  preserve: null,
  chivalry: new Set([...attackPrayers, ...strengthPrayers, ...defencePrayers]),
  piety: new Set([...attackPrayers, ...strengthPrayers, ...defencePrayers]),
  rigour: new Set([...attackPrayers, ...strengthPrayers, ...defencePrayers]),
  augury: new Set([...attackPrayers, ...strengthPrayers, ...defencePrayers]),
};
