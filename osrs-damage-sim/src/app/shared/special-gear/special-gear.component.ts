import { Component, Input } from '@angular/core';
import { GearSetup } from 'src/app/model/damage-sim/input-setup.model';
import { SpecialGear } from 'src/app/model/damage-sim/special-gear.model';
import { GearSlot } from 'src/app/model/osrs/gear-slot.enum';
import { Item } from 'src/app/model/osrs/item.model';

@Component({
  selector: 'app-special-gear',
  templateUrl: './special-gear.component.html',
  styleUrls: ['./special-gear.component.css'],
})
export class SpecialGearComponent {
  @Input()
  isMainGearSetup: boolean;

  @Input()
  gearSetup: GearSetup;

  @Input()
  specialGear: SpecialGear;

  @Input()
  slot: GearSlot;

  @Input()
  allDarts: Item[];

  GearSlot = GearSlot;
}
