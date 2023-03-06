import { Boost, ReplaceBoost } from './boost.model';

export const someBoosts: Set<Boost> = new Set(['smelling_salts']);

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

export const replaceBoosts: ReplaceBoost = {
  attack: new Set([...attackBoosts, ...multiBoosts]),
  super_attack: new Set([...attackBoosts, ...multiBoosts]),
  divine_super_attack: new Set([...attackBoosts, ...multiBoosts]),
  strength: new Set([...strengthBoosts, ...multiBoosts]),
  super_strength: new Set([...strengthBoosts, ...multiBoosts]),
  divine_super_strength: new Set([...strengthBoosts, ...multiBoosts]),
  combat: new Set(['attack', 'super_attack', 'divine_super_attack', ...strengthBoosts, ...multiBoosts]),
  super_combat: new Set(['attack', 'super_attack', 'divine_super_attack', ...strengthBoosts, ...multiBoosts]),
  divine_super_combat: new Set(['attack', 'super_attack', 'divine_super_attack', ...strengthBoosts, ...multiBoosts]),
  zamorak_brew: new Set([...attackBoosts, 'overload_plus', 'smelling_salts']),
  overload_plus: new Set([...attackBoosts, ...strengthBoosts, ...multiBoosts, ...magicBoosts, ...rangedBoosts]),
  smelling_salts: new Set([...attackBoosts, ...strengthBoosts, ...multiBoosts, ...magicBoosts, ...rangedBoosts]),
  magic: new Set([...magicBoosts, 'overload_plus', 'smelling_salts']),
  divine_magic: new Set([...magicBoosts, 'overload_plus', 'smelling_salts']),
  ancient_brew: new Set([...magicBoosts, 'overload_plus', 'smelling_salts']),
  forgotten_brew: new Set([...magicBoosts, 'overload_plus', 'smelling_salts']),
  imbued_heart: new Set([...magicBoosts, 'overload_plus', 'smelling_salts']),
  saturated_heart: new Set([...magicBoosts, 'overload_plus', 'smelling_salts']),
  ranging: new Set([...rangedBoosts, 'overload_plus', 'smelling_salts']),
  divine_ranging: new Set([...rangedBoosts, 'overload_plus', 'smelling_salts']),
  liquid_adrenaline: null,
};
