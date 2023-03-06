import { AttackType } from '../../model/osrs/item.model';

export interface QuickGear {
  label: string;
  itemIds: number[];
}

export type QuickGearSetups = {
  [attackType in AttackType]: QuickGear[];
};
