import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { filter, map, Observable } from 'rxjs';
import { RUNELITE_GEAR_URL } from '../constants.const';
import { RlGear } from '../model/damage-sim/rl-gear.model';

@Injectable({
  providedIn: 'root',
})
export class RlGearService {
  constructor(private http: HttpClient) {}

  getGear(): Observable<number[]> {
    return this.http
      .get<RlGear[]>(RUNELITE_GEAR_URL)
      .pipe(map((gear: RlGear[]) => gear.filter((item: RlGear) => item.id !== -1).map((item: RlGear) => item.id)));
  }
}
