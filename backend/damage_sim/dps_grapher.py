from damage_sim.damage_sim_graph import DamageSimGraph
from damage_sim.damage_sim_stats import DamageSimStats
from model.boost import Boost
from model.damage_sim_results.dps_graph_data import DpsGraphData, DpsGraphDpsData
from model.damage_sim_results.dps_grapher_results import DpsGrapherResults
from model.input_setup.dps_grapher_input import DpsGrapherInput, InputValueType, INPUT_VALUE_TYPE_LABEL, \
    STAT_DRAIN_INPUT_TYPE
from model.input_setup.input_gear_setup import InputGearSetup
from model.input_setup.stat_drain import StatDrain
from model.stat_drain_type import StatDrainType
from weapons.custom_weapon import CUSTOM_WEAPONS


class DpsGrapher:
    def __init__(self, damage_sim_graph: DamageSimGraph):
        self.damage_sim_graph = damage_sim_graph

    def run(self, dps_grapher_input: DpsGrapherInput) -> DpsGrapherResults:
        dps_data = []
        grapher_type = dps_grapher_input.settings.type
        input_value_range = range(dps_grapher_input.settings.min, dps_grapher_input.settings.max)
        for input_gear_setup in dps_grapher_input.input_setup.input_gear_setups:
            input_gear_setup_label = DamageSimStats.get_input_gear_setup_label(input_gear_setup).input_gear_setup_label

            Boost.apply_boosts(input_gear_setup.gear_setup_settings.combat_stats,
                               input_gear_setup.gear_setup_settings.boosts)

            dps_list = self.get_gear_setup_dps(input_gear_setup, grapher_type, input_value_range)
            dps_data.append(
                DpsGraphDpsData(label=input_gear_setup_label, dps=dps_list)
            )

        dps_graph_data = DpsGraphData(
            title="Dps: " + DamageSimStats.get_dps_graph_label(dps_grapher_input.input_setup.global_settings),
            x_values=input_value_range,
            x_label=INPUT_VALUE_TYPE_LABEL[grapher_type],
            dps_data=dps_data
        )

        graph = self.damage_sim_graph.get_dps_graphs(dps_graph_data)
        return DpsGrapherResults(
            graph=graph
        )

    def get_gear_setup_dps(self, input_gear_setup: InputGearSetup, grapher_type: InputValueType,
                           input_value_range) -> list[float]:
        npc = input_gear_setup.main_weapon.npc

        weapon_dps = []
        if grapher_type in STAT_DRAIN_INPUT_TYPE:
            weapon_dps = DpsGrapher.stat_drain_dps(input_gear_setup, grapher_type, input_value_range, npc)

        return weapon_dps

    @staticmethod
    def stat_drain_dps(input_gear_setup: InputGearSetup, grapher_type: InputValueType, input_value_range, npc):
        weapon_dps = []

        stat_drain = StatDrain(CUSTOM_WEAPONS[grapher_type.value], 0)
        for input_value in input_value_range:
            npc.combat_stats.set_stats(npc.base_combat_stats)
            stat_drain.value = input_value

            if stat_drain.weapon.stat_drain_type == StatDrainType.DAMAGE:
                stat_drain.weapon.drain_stats(npc, stat_drain.value)
            else:
                for hit in range(stat_drain.value):
                    stat_drain.weapon.drain_stats(npc, 1)
            input_gear_setup.main_weapon.update_dps_stats()
            weapon_dps.append(input_gear_setup.main_weapon.get_dps())

        return weapon_dps
