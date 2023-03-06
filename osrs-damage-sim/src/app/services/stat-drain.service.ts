import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { StatDrain } from '../model/damage-sim/stat-drain.model';

@Injectable({
  providedIn: 'root',
})
export class StatDrainService {
  globalStatDrain$: BehaviorSubject<StatDrain[]> = new BehaviorSubject([]);
}
