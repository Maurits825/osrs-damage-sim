import { Component, EventEmitter, Input, Output } from '@angular/core';
import { QuickGear } from 'src/app/model/damage-sim/quick-gear.model';
import { AttackType } from 'src/app/model/osrs/item.model';
import { quickGearSetups } from './quick-gear.const';

@Component({
  selector: 'app-quick-gear-select',
  templateUrl: './quick-gear-select.component.html',
  styleUrls: ['./quick-gear-select.component.css'],
})
export class QuickGearSelectComponent {
  @Input()
  attackType: AttackType;

  @Output()
  selectSetup = new EventEmitter<QuickGear>();

  AttackType: AttackType;
  quickGearSetups = quickGearSetups;

  onSelectSetup(setup: QuickGear): void {
    this.selectSetup.emit(setup);
  }
}
