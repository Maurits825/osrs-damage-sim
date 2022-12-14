export interface DamageSimResults {
    ttk_stats: SimStats[],
    total_dmg_stats: SimStats[][],
    attack_count_stats: SimStats[][],
    sim_dps_stats: SimStats[][],
    theoretical_dps: number[][],
    cumulative_chances: number[][]
}

export interface SimStats {
    average: string | number,
    maximum: string | number,
    minimum: string | number,
    most_frequent: string | number,
    
    chance_to_kill: string[] | number[],
    
    label: string | number,
}
