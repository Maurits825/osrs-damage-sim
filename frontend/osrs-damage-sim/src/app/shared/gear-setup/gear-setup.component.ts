import { Component, Inject, OnDestroy, OnInit, Optional, SkipSelf, ViewChild } from '@angular/core';
import { cloneDeep } from 'lodash-es';
import { forkJoin, Subject, takeUntil } from 'rxjs';
import { skip } from 'rxjs/operators';
import { ConditionComponent } from '../condition/condition.component';
import { GearSetupTabComponent } from '../gear-setup-tab/gear-setup-tab.component';
import { allBoosts } from '../../model/osrs/boost.model';
import { Condition } from '../../model/damage-sim/condition.model';
import { GearSlot } from '../../model/osrs/gear-slot.enum';
import { GearSetup } from '../../model/damage-sim/input-setup.model';
import { AttackType, Item } from '../../model/osrs/item.model';
import { SpecialGear } from '../../model/damage-sim/special-gear.model';
import { DamageSimService } from '../../services/damage-sim.service';
import { RlGearService } from '../../services/rl-gear.service';
import {
  DRAGON_DARTS_ID,
  UNARMED_EQUIVALENT_ID,
  DEFAULT_GEAR_SETUP,
  AUTOCAST_STLYE as AUTOCAST_STYLE,
} from './gear-setup.const';
import { Prayer } from 'src/app/model/osrs/prayer.model';
import { PrayerService } from 'src/app/services/prayer.service';
import { SpecialGearService } from 'src/app/services/special-gear.service';
import { GEAR_SETUP_TOKEN } from 'src/app/model/damage-sim/injection-token.const';
import { QuickGear } from 'src/app/model/damage-sim/quick-gear.model';
import { GearSetupPreset } from 'src/app/model/damage-sim/gear-preset.model';

@Component({
  selector: 'app-gear-setup.col-md-6',
  templateUrl: './gear-setup.component.html',
  styleUrls: ['./gear-setup.component.css'],
})
export class GearSetupComponent implements OnInit, OnDestroy {
  @ViewChild(ConditionComponent) conditionComponent: ConditionComponent;

  setupCount: number;
  isMainGearSetup = false;
  gearSetupTabRef: GearSetupTabComponent;

  GearSlot = GearSlot;

  allGearSlots: GearSlot[] = Object.values(GearSlot);

  allGearSlotItems: Record<GearSlot, Item[]>;

  gearSetupPresets: GearSetupPreset[];

  allBoosts = allBoosts;

  attackStyles: string[];
  allSpells: string[];

  attackType: AttackType = 'melee';

  allDarts: Item[];

  specialGear: SpecialGear = {
    isSpecialWeapon: false,
    isSlayerHelm: false,
    isWildernessWeapon: false,
    isDharokSet: false,
    isSpecialBolt: false,
    isBlowpipe: false,
    isPickaxe: false,
  };

  Item: Item;

  private destroyed$ = new Subject();

  constructor(
    private damageSimservice: DamageSimService,
    private rlGearService: RlGearService,
    private prayerService: PrayerService,
    private specialGearService: SpecialGearService,
    @SkipSelf() @Optional() @Inject(GEAR_SETUP_TOKEN) public gearSetup: GearSetup
  ) {}

  ngOnDestroy(): void {
    this.destroyed$.next(true);
    this.destroyed$.complete();
  }

  ngOnInit(): void {
    forkJoin({
      allGearSlotItems: this.damageSimservice.allGearSlotItems$,
      gearSetupPresets: this.damageSimservice.gearSetupPresets$,
      allSpells: this.damageSimservice.allSpells$,
      allDarts: this.damageSimservice.allDarts$,
    }).subscribe(({ allGearSlotItems, gearSetupPresets, allSpells, allDarts }) => {
      this.allGearSlotItems = allGearSlotItems;
      this.gearSetupPresets = gearSetupPresets;
      this.allSpells = allSpells;
      this.allDarts = allDarts;

      if (this.gearSetup) {
        this.setGearSetup(this.gearSetup);
      } else {
        this.gearSetup = cloneDeep(DEFAULT_GEAR_SETUP);

        this.gearSetup.blowpipeDarts = this.allDarts.find((dart: Item) => dart.id === DRAGON_DARTS_ID);

        this.gearSetup.prayers = new Set(this.prayerService.globalPrayers$.getValue()['melee']);
        this.attackStyles = this.getItem(GearSlot.Weapon, UNARMED_EQUIVALENT_ID).attackStyles;
      }

      this.prayerService.globalPrayers$
        .pipe(takeUntil(this.destroyed$), skip(1))
        .subscribe(
          (prayers: Record<AttackType, Set<Prayer>>) => (this.gearSetup.prayers = new Set(prayers[this.attackType]))
        );
    });
  }

  getItem(slot: GearSlot, id: number): Item {
    return this.allGearSlotItems[slot].find((item: Item) => item.id === id);
  }

  getGearSetup(): GearSetup {
    return this.gearSetup;
  }

  loadRlGear(): void {
    this.rlGearService.getGear().subscribe((gearIds: number[]) => {
      this.allGearSlots.forEach((slot: GearSlot) => {
        this.gearSlotChange(null, slot);
        this.gearSetup.gear[slot] = null;

        gearIds.forEach((itemId: number) => {
          const item = this.getItem(slot, itemId);
          if (item) {
            this.gearSlotChange(item, slot);
            this.gearSetup.gear[slot] = item;
          }
        });
      });
    });
  }

  loadGearSetupPreset(gearSetupPreset: GearSetupPreset) {
    this.setCurrentGearByIds(gearSetupPreset.gearIds);
    this.gearSetup.setupName = gearSetupPreset.name;
    this.gearSetup.presetName = gearSetupPreset.name;
  }

  setCurrentGearByGearSlotAndId(gearIds: Record<GearSlot, number>): void {
    this.allGearSlots.forEach((slot: GearSlot) => {
      if (gearIds[slot]) {
        const item = this.getItem(slot, gearIds[slot]);
        this.gearSlotChange(item, slot);
        this.gearSetup.gear[slot] = item;
      } else {
        this.gearSlotChange(null, slot);
        this.gearSetup.gear[slot] = null;
      }
    });
  }

  setCurrentGearByIds(gearIds: number[], clearEmtpy = false): void {
    this.allGearSlots.forEach((slot: GearSlot) => {
      if (clearEmtpy) {
        this.gearSlotChange(null, slot);
        this.gearSetup.gear[slot] = null;
      }

      gearIds.forEach((itemId: number) => {
        const item = this.getItem(slot, itemId);
        if (item) {
          this.gearSlotChange(item, slot);
          this.gearSetup.gear[slot] = item;
        }
      });
    });
  }

  gearSlotChange(item: Item, slot: GearSlot): void {
    this.gearSetup.gear[slot] = item;
    this.gearSetup.presetName = null;

    if (slot === GearSlot.Weapon) {
      const itemId = item?.id || UNARMED_EQUIVALENT_ID;
      this.gearSetup.setupName = 'Unarmed';
      this.attackType = 'melee';

      if (item) {
        this.gearSetup.setupName = item.name;
        this.attackType = item.attackType;
      }

      this.gearSetup.prayers = new Set(this.prayerService.globalPrayers$.getValue()[this.attackType]);

      this.updateAttackStyle(itemId);
    }

    this.updateSpecialGear();
  }

  updateAttackStyle(itemId: number): void {
    this.attackStyles = this.getItem(GearSlot.Weapon, itemId).attackStyles;
    if (this.attackStyles.includes(AUTOCAST_STYLE)) {
      this.gearSetup.attackStyle = AUTOCAST_STYLE;
    } else {
      this.gearSetup.attackStyle = this.attackStyles[1]; //second attack style is most commonly used
    }
  }

  togglePrayer(prayer: Prayer): void {
    this.prayerService.togglePrayer(prayer, this.gearSetup.prayers);
  }

  removeGearSetup(): void {
    this.gearSetupTabRef.removeGearSetup(this.setupCount);
  }

  setGearSetup(gearSetup: GearSetup): void {
    this.gearSetup = cloneDeep(gearSetup);

    const itemId = this.gearSetup.gear[GearSlot.Weapon]?.id || UNARMED_EQUIVALENT_ID;

    const weapon = this.getItem(GearSlot.Weapon, itemId);
    this.attackStyles = weapon.attackStyles;
    this.attackType = weapon.attackType;
    this.updateSpecialGear();
  }

  updateConditions(conditions: Condition[]): void {
    this.gearSetup.conditions = conditions;
  }

  duplicateGearSetup(): void {
    this.gearSetupTabRef.addNewGearSetup(this.gearSetup);
  }

  updateSpecialGear(): void {
    this.specialGear = this.specialGearService.getSpecialGear(this.gearSetup);
  }

  selectedSpellChange(): void {
    if (this.attackStyles.includes(AUTOCAST_STYLE)) {
      this.gearSetup.attackStyle = AUTOCAST_STYLE;
    } else {
      this.gearSetup.attackStyle = null;
    }
  }

  selectQuickGearSetup(quickGear: QuickGear): void {
    this.setCurrentGearByIds(quickGear.itemIds);
  }
}
