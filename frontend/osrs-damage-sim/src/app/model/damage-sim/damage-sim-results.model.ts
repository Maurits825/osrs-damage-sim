import { Graphs } from './graphs.model';

export interface InputGearSetupLabels {
  input_gear_setup_label: string;
  gear_setup_settings_label: string;
  all_weapon_labels: string[];
}

export interface DamageSimResults {
  error: string | null;

  labels: InputGearSetupLabels[];
  ttk_stats: SimStats[];
  total_damage_stats: SimStats[][];
  attack_count_stats: SimStats[][];
  sim_dps_stats: SimStats[][];
  theoretical_dps: number[][];
  cumulative_chances: number[][];
  max_hit: number[][];
  accuracy: number[][];
  graphs: Graphs;
}

export interface SimStats {
  average: string | number;
  maximum: string | number;
  minimum: string | number;
  most_frequent: string | number;

  chance_to_kill: string[] | number[];

  label: string | number;
}
