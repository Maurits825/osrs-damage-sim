import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Condition } from '../model/condition.model';

@Component({
  selector: 'app-condition',
  templateUrl: './condition.component.html',
  styleUrls: ['./condition.component.css']
})
export class ConditionComponent implements OnInit {
  conditionVariables = {
    "NPC_HITPOINTS": "Npc hitpoints",
    "DMG_DEALT": "Damage dealt",
  }
  
  conditionComparisons1 = {
    "AND": "and",
    "OR": "or",
  }

  conditionComparisons2 = {
    "EQUAL": "==",
    "GRT_THAN": ">",
    "LESS_THAN": "<",
    "GRT_EQ_THAN": ">=",
    "LESS_EQ_THAN": "<=",
  }

  @Input() isFill: boolean;
  @Output() conditionsChanged = new EventEmitter<Condition[]>();
  conditions: Condition[] = [];

  constructor() { }

  ngOnInit(): void {
  }

  addCondition(): void {
    this.conditions.push({
      variable: "NPC_HITPOINTS",
      comparison: "==",
      value: 0,
      nextComparison: "AND",
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
