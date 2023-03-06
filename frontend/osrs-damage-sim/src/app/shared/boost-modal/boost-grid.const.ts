import { Boost } from 'src/app/model/osrs/boost.model';

const attackBoosts: Set<Boost> = new Set(['attack', 'super_attack', 'divine_super_attack', 'zamorak_brew']);
const strengthBoosts: Set<Boost> = new Set(['strength', 'super_strength', 'divine_super_strength']);
const multiBoosts: Set<Boost> = new Set([
  'combat',
  'super_combat',
  'divine_super_combat',
  'overload_plus',
  'smelling_salts',
]);
const magicBoosts: Set<Boost> = new Set([
  'magic',
  'divine_magic',
  'ancient_brew',
  'forgotten_brew',
  'imbued_heart',
  'saturated_heart',
]);
const rangedBoosts: Set<Boost> = new Set(['ranging', 'divine_ranging']);
const otherBoosts: Set<Boost> = new Set(['liquid_adrenaline']);

export const gridBoosts: Set<Boost>[] = [
  attackBoosts,
  strengthBoosts,
  multiBoosts,
  rangedBoosts,
  magicBoosts,
  otherBoosts,
];
