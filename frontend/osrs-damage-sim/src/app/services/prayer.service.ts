import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { AttackType } from '../model/osrs/item.model';
import { replacePrayers } from '../model/osrs/prayer-replace.const';
import { Prayer } from '../model/osrs/prayer.model';

@Injectable({
  providedIn: 'root',
})
export class PrayerService {
  globalPrayers$: BehaviorSubject<Record<AttackType, Set<Prayer>>> = new BehaviorSubject(null);

  togglePrayer(prayer: Prayer, selectedPrayers: Set<Prayer>): void {
    if (selectedPrayers.has(prayer)) {
      selectedPrayers.delete(prayer);
    } else {
      if (replacePrayers[prayer]) {
        for (const replacePrayer of replacePrayers[prayer]) {
          selectedPrayers.delete(replacePrayer);
        }
      }
      selectedPrayers.add(prayer);
    }
  }
}
