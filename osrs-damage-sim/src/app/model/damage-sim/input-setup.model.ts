import { Boost } from '../osrs/boost.model';
import { Condition } from './condition.model';
import { GearSlot } from '../osrs/gear-slot.enum';
import { Item } from '../osrs/item.model';
import { CombatStats } from '../osrs/skill.type';
import { Prayer } from '../osrs/prayer.model';
import { StatDrain } from './stat-drain.model';
import { Npc } from '../osrs/npc.model';

export interface InputSetup {
  globalSettings: GlobalSettings;
  inputGearSetups: InputGearSetup[];
}

export interface GlobalSettings {
  iterations: number;
  npc: Npc;

  raidLevel: number;
  pathLevel: number;

  teamSize: number;
}

export interface InputGearSetup {
  gearSetupSettings: GearSetupSettings;
  mainGearSetup: GearSetup;
  fillGearSetups: GearSetup[];
}

export interface GearSetupSettings {
  statDrains: StatDrain[];
  combatStats: CombatStats;
  boosts: Set<Boost>;
}

export interface GearSetup {
  setupName: string;
  presetName: string;

  gear: Record<GearSlot, Item>;
  blowpipeDarts: Item;

  attackStyle: string;
  spell: string;

  isSpecial: boolean;
  prayers: Set<Prayer>;

  conditions: Condition[];

  statDrain: StatDrain[];

  isOnSlayerTask: boolean;
  isInWilderness: boolean;

  currentHp: number;

  miningLvl: number;

  isKandarinDiary: boolean;
}
