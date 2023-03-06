import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Condition } from '../../model/damage-sim/condition.model';

@Component({
  selector: 'app-condition',
  templateUrl: './condition.component.html',
  styleUrls: ['./condition.component.css'],
})
export class ConditionComponent implements OnInit {
  @Input()
  initialConditions: Condition[];

  conditionVariables = {
    NPC_HITPOINTS: 'Npc hitpoints',
    DMG_DEALT: 'Damage dealt',
    ATTACK_COUNT: 'Attack count',
  };

  conditionComparisons1 = {
    AND: 'and',
    OR: 'or',
  };

  conditionComparisons2 = {
    EQUAL: '==',
    GRT_THAN: '>',
    LESS_THAN: '<',
    GRT_EQ_THAN: '>=',
    LESS_EQ_THAN: '<=',
  };

  @Output() conditionsChanged = new EventEmitter<Condition[]>();
  conditions: Condition[] = [];

  ngOnInit(): void {
    this.conditions = this.initialConditions;
  }

  addCondition(): void {
    this.conditions.push({
      variable: 'NPC_HITPOINTS',
      comparison: '==',
      value: 0,
      nextComparison: 'AND',
    });

    this.conditionsChanged.emit(this.conditions);
  }

  removeCondition(condition: Condition): void {
    const index = this.conditions.indexOf(condition);
    if (index >= 0) {
      this.conditions.splice(index, 1);
    }

    this.conditionsChanged.emit(this.conditions);
  }
}
