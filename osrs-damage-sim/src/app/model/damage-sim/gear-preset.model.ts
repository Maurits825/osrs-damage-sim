import { AttackType } from '../osrs/item.model';

export interface GearSetupPreset {
  name: string;
  gearIds: number[];
  icon: string;
  attackType: AttackType;
}
