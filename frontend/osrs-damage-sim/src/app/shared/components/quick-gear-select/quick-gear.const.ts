import { QuickGearSetups } from 'src/app/model/damage-sim/quick-gear.model';

export const quickGearSetups: QuickGearSetups = {
  melee: [
    {
      label: 'Void melee',
      itemIds: [11665, 13072, 13073, 8842],
    },
    {
      label: 'Torva',
      itemIds: [26382, 26384, 26386],
    },
    {
      label: 'Bandos',
      itemIds: [11832, 11834],
    },
    {
      label: 'Inquisitor',
      itemIds: [24419, 24420, 24421],
    },
    {
      label: 'Justiciar',
      itemIds: [22326, 22327, 22328],
    },
  ],

  ranged: [
    {
      label: 'Void range',
      itemIds: [11664, 13072, 13073, 8842],
    },
    {
      label: 'Masori',
      itemIds: [27235, 27238, 27241],
    },
    {
      label: 'Armadyl',
      itemIds: [11826, 11828, 11830],
    },
    {
      label: 'Blessed dhide',
      itemIds: [10386, 10388],
    },
    {
      label: 'Crystal',
      itemIds: [23971, 23975, 23979],
    },
  ],

  magic: [
    {
      label: 'Void mage',
      itemIds: [11663, 13072, 13073, 8842],
    },
    {
      label: 'Ancestral',
      itemIds: [21018, 21021, 21024],
    },
    {
      label: 'Ahrim',
      itemIds: [4712, 4714],
    },
    {
      label: 'Mystic',
      itemIds: [4101, 4103],
    },
  ],
};

export const quickExtraGearSetups: QuickGearSetups = {
  melee: [
    {
      label: 'Max',
      itemIds: [19553, 22981, 13239],
    },
    {
      label: 'Mid',
      itemIds: [6585, 7462, 11840],
    },
  ],

  ranged: [
    {
      label: 'Max',
      itemIds: [19547, 26235, 13237],
    },
    {
      label: 'Mid',
      itemIds: [6585, 7462, 19933],
    },
  ],

  magic: [
    {
      label: 'Max',
      itemIds: [12002, 19544, 13235],
    },
    {
      label: 'Mid',
      itemIds: [6585, 7462],
    },
  ],
};
