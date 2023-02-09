import { Component, Input } from '@angular/core';
import { GearInputSetup } from 'src/app/model/damage-sim/input-setup.model';
import { SpecialGear } from 'src/app/model/damage-sim/special-gear.model';
import { GearSlot } from 'src/app/model/osrs/gear-slot.enum';
import { Item } from 'src/app/model/osrs/item.model';
import { BLOWPIPE_ID } from '../gear-setup/gear-setup.const';

@Component({
  selector: 'app-special-gear',
  templateUrl: './special-gear.component.html',
  styleUrls: ['./special-gear.component.css'],
})
export class SpecialGearComponent {
  @Input()
  gearInputSetup: GearInputSetup;

  @Input()
  specialGear: SpecialGear;

  @Input()
  selectedDart: Item;

  @Input()
  slot: GearSlot;

  @Input()
  allDarts: Item[];

  GearSlot = GearSlot;
  BLOWPIPE_ID = BLOWPIPE_ID;
}