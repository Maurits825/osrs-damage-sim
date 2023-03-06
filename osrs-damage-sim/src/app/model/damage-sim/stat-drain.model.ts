export const allStatDrains = ['Dragon warhammer', 'Bandos godsword', 'Arclight'] as const;

export type StatDrainItem = typeof allStatDrains[number];

export interface StatDrain {
  name: StatDrainItem;
  value: number;
}
