from model.condition import ConditionComparison, Condition, ConditionVariables


class ConditionEvaluator:
    @staticmethod
    def evaluate_comparison(comparison: ConditionComparison, value1, value2) -> bool:
        if comparison == ConditionComparison.EQUAL:
            return value1 == value2
        elif comparison == ConditionComparison.GRT_THAN:
            return value1 > value2
        elif comparison == ConditionComparison.LESS_THAN:
            return value1 < value2
        elif comparison == ConditionComparison.GRT_EQ_THAN:
            return value1 >= value2
        elif comparison == ConditionComparison.LESS_EQ_THAN:
            return value1 <= value2

    @staticmethod
    def evaluate_condition(conditions: list[Condition], npc_hitpoints, dmg_dealt, attack_count):
        if len(conditions) == 0:
            return True

        bool_conditions = []

        for condition in conditions:
            if condition.variable == ConditionVariables.NPC_HITPOINTS:
                variable = npc_hitpoints
            elif condition.variable == ConditionVariables.DMG_DEALT:
                variable = dmg_dealt
            elif condition.variable == ConditionVariables.ATTACK_COUNT:
                variable = attack_count
            else:
                variable = 0

            bool_conditions.append(ConditionEvaluator.evaluate_comparison(condition.comparison,
                                                                          variable, condition.value))

        # TODO multiple conditions with mixed and/or doesnt make any sense, no grouping yet
        condition_result = bool_conditions[0]
        for idx, condition in enumerate(conditions[:-1]):
            condition_result = True
            if condition.nextComparison == ConditionComparison.AND:
                condition_result = condition_result and (bool_conditions[idx] and bool_conditions[idx + 1])
            elif condition.nextComparison == ConditionComparison.OR:
                condition_result = condition_result and (bool_conditions[idx] or bool_conditions[idx + 1])

        return condition_result
