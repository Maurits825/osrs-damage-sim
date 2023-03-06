from damage_sim.damage_sim import DamageSim
from damage_sim.damage_sim_graph import DamageSimGraph
from damage_sim.damage_sim_stats import DamageSimStats
from model.damage_sim_results import DamageSimResults, TotalDamageSimData, GearSetupDpsStats
from model.input_setup.global_settings import GlobalSettings
from model.input_setup.input_gear_setup import InputGearSetup
from model.input_setup.input_setup import InputSetup


class DamageSimRunner:
    def __init__(self):
        self.damage_sim_graph = DamageSimGraph()

    def run(self, input_setup: InputSetup) -> DamageSimResults:

        damage_sim_results = DamageSimResults([], [], [], [], [], [], [], [], [], {})  # TODO better way?
        ttk_tick_stats = []
        ttk_list = []
        for input_gear_setup in input_setup.input_gear_setups:
            input_gear_setup_labels = DamageSimStats.get_input_gear_setup_label(input_gear_setup)
            damage_sim_results.labels.append(input_gear_setup_labels)

            sim_data, gear_setup_dps_stats = self.run_damage_sim(input_setup.global_settings, input_gear_setup)

            damage_sim_results.theoretical_dps.append(gear_setup_dps_stats.theoretical_dps)
            damage_sim_results.max_hit.append(gear_setup_dps_stats.max_hit)
            damage_sim_results.accuracy.append(gear_setup_dps_stats.accuracy)

            ttk_tick_stat = DamageSimStats.populate_damage_sim_results(damage_sim_results, sim_data)
            ttk_tick_stats.append(ttk_tick_stat)

            ttk_list.append(sim_data.ticks_to_kill)

        graph_labels = [label.input_gear_setup_label for label in damage_sim_results.labels]
        min_ticks, max_ticks = DamageSimStats.get_min_and_max_ticks(ttk_tick_stats)
        damage_sim_results.graphs = self.damage_sim_graph.get_all_graphs(
            min_ticks, max_ticks, graph_labels, input_setup, ttk_list
        )

        return damage_sim_results

    def run_damage_sim(self, global_settings: GlobalSettings, input_gear_setup: InputGearSetup
                       ) -> (TotalDamageSimData, GearSetupDpsStats):
        total_damage_sim_data = TotalDamageSimData([], [], [], [])
        damage_sim = DamageSim(global_settings.npc, input_gear_setup)

        gear_setup_dps_stats = damage_sim.get_weapon_dps_stats()

        for i in range(global_settings.iterations):
            dmg_sim_data = damage_sim.run()
            total_damage_sim_data.ticks_to_kill.append(dmg_sim_data.ticks_to_kill)
            total_damage_sim_data.gear_total_dmg.append(dmg_sim_data.gear_total_dmg)
            total_damage_sim_data.gear_attack_count.append(dmg_sim_data.gear_attack_count)
            total_damage_sim_data.gear_dps.append(dmg_sim_data.gear_dps)
        return total_damage_sim_data, gear_setup_dps_stats
