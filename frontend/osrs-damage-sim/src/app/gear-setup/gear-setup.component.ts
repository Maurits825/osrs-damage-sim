import { Component, OnInit } from '@angular/core';
import { GearSetupTabComponent } from '../gear-setup-tab/gear-setup-tab.component';
import { Item } from '../model/item.model';
import { DamageSimService } from '../services/damage-sim.service';
import { GearSetupService } from '../services/gear-setups.service';
import { RlGearService } from '../services/rl-gear.service';

@Component({
  selector: 'app-gear-setup',
  templateUrl: './gear-setup.component.html',
  styleUrls: ['./gear-setup.component.css']
})
export class GearSetupComponent implements OnInit {
  setupCount!: number;
  gearSetUpTabRef!: GearSetupTabComponent;

  gearSlots: Array<any> = [0, 1, 2, 3, 4, 5, 7, 9, 10, 12, 13];

  currentGear: Record<number, Item> = {};

  allGearSlotItems: Record<number, Record<number, Item>> = {};

  gearSetups: Record<string, Record<number, Item>> = {};
  selectedGearSetup: string = "";

  setupName: string = "";

  attackStyles: string[] = [];
  selectedAttackStyle: string = null;

  prayers: string[] = ["eagle_eye", "rigour", "chivalry", "piety"];
  selectedPrayers: string[] = [];

  attackCount: number = 0;
  isSpecialAttack: boolean = false;

  constructor(
    private damageSimservice: DamageSimService,
    private rlGearService: RlGearService,
    private gearSetupService: GearSetupService,
    ) {}

  ngOnInit(): void {
    this.damageSimservice.getGearSlotItems().subscribe((gearSlotItems: Record<number, Record<number, Item>>) => {
      this.allGearSlotItems = gearSlotItems;
    });

    this.gearSetupService.getGearSetups().subscribe((gearSetups: Record<string, Record<number, Item>>) => {
      this.gearSetups = gearSetups;
    });

    this.damageSimservice.getAttackStyles(0).subscribe((styles: string[]) => {
      this.attackStyles = styles;
    });
  }

  clearAllGear(): void {
    this.selectedGearSetup = null;
    this.setupName = "";
    
    this.gearSlots.forEach((slot: number) => {
      this.clearGearSlot(slot);
    });

    this.selectedPrayers = [];
    this.attackCount = 0;
    this.isSpecialAttack = false;
  }

  loadRlGear(): void {
    this.selectedGearSetup = null;

    this.rlGearService.getGear()
      .subscribe((gearSlotItem: Record<number, Item>) => {
        this.gearSlots.forEach((slot: number) => {
          if (gearSlotItem[slot]?.name) {
            this.currentGear[slot] = this.allGearSlotItems[slot][gearSlotItem[slot].id];

            if (slot == 3) {
              this.setupName = gearSlotItem[slot].name;
              this.updateAttackStyle(gearSlotItem[slot].id);
            }
          }
          else {
            this.clearGearSlot(slot);
          }
        });
    });
  }

  clearGearSlot(slot: number): void {
    this.currentGear[slot] = null;

    if (slot == 3) {
      this.damageSimservice.getAttackStyles(0).subscribe((styles: string[]) => {
        this.attackStyles = styles;
        this.selectedAttackStyle = null;
      });
    }
  }

  loadGearSetup(setupName: string) {
    const gearSetup = this.gearSetups[setupName];
    this.setupName = setupName;

    this.gearSlots.forEach((slot: number) => {
      if (gearSetup[slot]?.name) {
        this.currentGear[slot] = this.allGearSlotItems[slot][gearSetup[slot].id];

        if (slot == 3) {
          this.updateAttackStyle(gearSetup[slot].id);
        }
      }
      else {
        this.clearGearSlot(slot);
      }
    });
  }

  gearSlotChange(item: Item, slot: number): void {
    this.selectedGearSetup = null;

    if (slot == 3) {
      this.updateAttackStyle(item.id);

      if (!this.setupName) {
        this.setupName = item.name;
      }
    }
  }

  updateAttackStyle(itemId: number): void {
    this.damageSimservice.getAttackStyles(itemId).subscribe((styles: string[]) => {
      this.attackStyles = styles;
      this.selectedAttackStyle = null;
    });
  }

  addPrayer(prayer: string): void {
    this.selectedPrayers.push(prayer);
  }

  removePrayer(prayer: string): void {
    this.selectedPrayers = this.selectedPrayers.filter(p => p !== prayer);
  }

  removeGearSetup(): void {
    this.gearSetUpTabRef.removeGearSetup(this.setupCount);
  }
}
