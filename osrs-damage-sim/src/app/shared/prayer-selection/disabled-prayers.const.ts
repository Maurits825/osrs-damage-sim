import { Prayer } from 'src/app/model/osrs/prayer.model';

export const disabledPrayers: Set<Prayer> = new Set([
  'protect_from_magic',
  'protect_from_missiles',
  'protect_from_melee',
  'retribution',
  'redemption',
  'smite',
  'rapid_heal',
  'rapid_restore',
  'protect_item',
  'preserve',
]);
