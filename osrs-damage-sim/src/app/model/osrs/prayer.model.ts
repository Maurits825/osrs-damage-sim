export const allPrayers = [
  'thick_skin',
  'burst_of_strength',
  'clarity_of_thought',
  'sharp_eye',
  'mystic_will',
  'rock_skin',
  'superhuman_strength',
  'improved_reflexes',
  'rapid_heal',
  'rapid_restore',
  'protect_item',
  'hawk_eye',
  'mystic_lore',
  'steel_skin',
  'ultimate_strength',
  'incredible_reflexes',
  'protect_from_magic',
  'protect_from_missiles',
  'protect_from_melee',
  'eagle_eye',
  'mystic_might',
  'retribution',
  'redemption',
  'smite',
  'preserve',
  'chivalry',
  'piety',
  'rigour',
  'augury',
] as const;

export type Prayer = typeof allPrayers[number];

export type ReplacePrayer = {
  [name in Prayer]: Set<Prayer>;
};
