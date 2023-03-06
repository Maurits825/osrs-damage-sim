import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { CombatStats } from '../model/osrs/skill.type';

@Injectable({
  providedIn: 'root',
})
export class CombatStatService {
  globalCombatStats$: BehaviorSubject<CombatStats> = new BehaviorSubject({
    attack: 99,
    strength: 99,
    ranged: 99,
    magic: 99,
    hitpoints: 99,
  });
}
