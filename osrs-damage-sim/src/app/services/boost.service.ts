import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { replaceBoosts } from '../model/osrs/boost-replace.const';
import { Boost } from '../model/osrs/boost.model';

@Injectable({
  providedIn: 'root',
})
export class BoostService {
  globalBoosts$: BehaviorSubject<Set<Boost>> = new BehaviorSubject(new Set());

  toggleBoost(boost: Boost, selectedBoosts: Set<Boost>): void {
    if (selectedBoosts.has(boost)) {
      selectedBoosts.delete(boost);
    } else {
      if (replaceBoosts[boost]) {
        for (const replacePrayer of replaceBoosts[boost]) {
          selectedBoosts.delete(replacePrayer);
        }
      }
      selectedBoosts.add(boost);
    }
  }
}
