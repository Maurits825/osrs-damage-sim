import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable, shareReplay } from 'rxjs';
import { environment } from 'src/environments/environment';
import { DamageSimResults } from '../model/damage-sim/damage-sim-results.model';
import { GearSetupPreset } from '../model/damage-sim/gear-preset.model';
import { GearSlot } from '../model/osrs/gear-slot.enum';
import { Item } from '../model/osrs/item.model';
import { Npc } from '../model/osrs/npc.model';

@Injectable({
  providedIn: 'root',
})
export class DamageSimService {
  public allGearSlotItems$: Observable<Record<GearSlot, Item[]>>;
  public gearSetupPresets$: Observable<GearSetupPreset[]>;
  public allSpells$: Observable<string[]>;
  public allNpcs$: Observable<Npc[]>;
  public allDarts$: Observable<Item[]>;

  private damageSimServiceUrl = environment.OSRS_DAMAGE_SIM_SERVICE_URL;

  constructor(private http: HttpClient) {
    this.allGearSlotItems$ = this.getGearSlotItems().pipe(shareReplay(1));
    this.gearSetupPresets$ = this.getGearSetupPresets().pipe(
      map((presets: GearSetupPreset[]) =>
        presets.sort((a: GearSetupPreset, b: GearSetupPreset) => a.name.localeCompare(b.name))
      ),
      shareReplay(1)
    );
    this.allSpells$ = this.getSpells().pipe(shareReplay(1));
    this.allNpcs$ = this.getNpcs().pipe(shareReplay(1));
    this.allDarts$ = this.getDarts().pipe(shareReplay(1));
  }

  public getStatus(): Observable<string> {
    return this.http.get<string>(this.damageSimServiceUrl + '/status');
  }

  public runDamageSim(inputSetupJson: string): Observable<DamageSimResults> {
    const options = { headers: { 'Content-Type': 'application/json' } };
    return this.http.post<DamageSimResults>(this.damageSimServiceUrl + '/run-damage-sim', inputSetupJson, options);
  }

  private getGearSlotItems(): Observable<Record<GearSlot, Item[]>> {
    return this.http.get<Record<GearSlot, Item[]>>(this.damageSimServiceUrl + '/gear-slot-items');
  }

  private getSpells(): Observable<string[]> {
    return this.http.get<string[]>(this.damageSimServiceUrl + '/all-spells').pipe(map((obj) => Object.keys(obj)));
  }

  private getNpcs(): Observable<Npc[]> {
    return this.http.get<Npc[]>(this.damageSimServiceUrl + '/npcs');
  }

  private getGearSetupPresets(): Observable<GearSetupPreset[]> {
    return this.http.get<GearSetupPreset[]>(this.damageSimServiceUrl + '/gear-setup-presets');
  }

  private getDarts(): Observable<Item[]> {
    return this.allGearSlotItems$.pipe(
      map((gearSlotItem: Record<GearSlot, Item[]>) =>
        gearSlotItem[GearSlot.Weapon].filter((item: Item) => item.name.match('dart$'))
      )
    );
  }
}
