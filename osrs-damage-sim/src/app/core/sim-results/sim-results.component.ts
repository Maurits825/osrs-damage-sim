import { Component, Input } from '@angular/core';
import { DamageSimResults } from '../../model/damage-sim/damage-sim-results.model';

@Component({
  selector: 'app-sim-results',
  templateUrl: './sim-results.component.html',
  styleUrls: ['./sim-results.component.css'],
})
export class SimResultsComponent {
  @Input()
  damageSimResults: DamageSimResults;

  targetTimeChance: number[];

  targetTimeChanged(targetTime: string): void {
    if (!targetTime) {
      return;
    }

    const matches = targetTime.match(/^([0-9]*):([0-9]*)\.([0-9]*)$/);

    const targetSeconds = +matches[1] * 60 + +matches[2] + +matches[3] / 10;
    const targetTicks = Math.ceil(targetSeconds / 0.6);

    this.targetTimeChance = [];
    this.damageSimResults.cumulative_chances.forEach((chances: number[]) => {
      this.targetTimeChance.push(chances[targetTicks]);
    });
  }
}
