import { Component, EventEmitter, Input, Output } from '@angular/core';
import { allStatDrains, StatDrain } from 'src/app/model/damage-sim/stat-drain.model';
import { statDrainLabels } from './stat-drain-labels.const';

@Component({
  selector: 'app-stat-drain-selection',
  templateUrl: './stat-drain-selection.component.html',
  styleUrls: ['./stat-drain-selection.component.css'],
})
export class StatDrainSelectionComponent {
  @Input()
  statDrains: StatDrain[];

  @Output()
  statDrainsChanged = new EventEmitter<StatDrain[]>();

  allStatDrains = [...allStatDrains];

  statDrainLabels = statDrainLabels;

  addStatDrain(): void {
    this.statDrains.push({
      name: 'Dragon warhammer',
      value: 0,
    });

    this.statDrainsChanged.emit(this.statDrains);
  }

  removeStatDrain(statDrain: StatDrain): void {
    const index = this.statDrains.indexOf(statDrain);
    if (index >= 0) {
      this.statDrains.splice(index, 1);
    }

    this.statDrainsChanged.emit(this.statDrains);
  }
}
