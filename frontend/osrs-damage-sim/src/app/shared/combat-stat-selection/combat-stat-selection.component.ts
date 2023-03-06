import { Component, EventEmitter, Input, Output } from '@angular/core';
import { allSkills, CombatStats } from 'src/app/model/osrs/skill.type';

@Component({
  selector: 'app-combat-stat-selection',
  templateUrl: './combat-stat-selection.component.html',
  styleUrls: ['./combat-stat-selection.component.css'],
})
export class CombatStatSelectionComponent {
  @Input()
  combatStats: CombatStats;

  @Output()
  combatStatsChanged = new EventEmitter<CombatStats>();

  allSkills = allSkills;

  onCombatStatsChanged(): void {
    this.combatStatsChanged.emit(this.combatStats);
  }
}
