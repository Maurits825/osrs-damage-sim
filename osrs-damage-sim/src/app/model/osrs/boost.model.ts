export const allBoosts = [
  'attack',
  'super_attack',
  'divine_super_attack',
  'strength',
  'super_strength',
  'divine_super_strength',
  'combat',
  'super_combat',
  'divine_super_combat',
  'zamorak_brew',
  'overload_plus',
  'smelling_salts',
  'magic',
  'divine_magic',
  'ancient_brew',
  'forgotten_brew',
  'imbued_heart',
  'saturated_heart',
  'ranging',
  'divine_ranging',
  'liquid_adrenaline',
] as const;

export type Boost = typeof allBoosts[number];

export type ReplaceBoost = {
  [name in Boost]: Set<Boost>;
};
