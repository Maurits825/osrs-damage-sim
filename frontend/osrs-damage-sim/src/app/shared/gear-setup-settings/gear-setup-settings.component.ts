import { Component, OnDestroy, OnInit } from '@angular/core';
import { takeUntil, Subject } from 'rxjs';
import { GearSetupSettings } from 'src/app/model/damage-sim/input-setup.model';
import { StatDrain } from 'src/app/model/damage-sim/stat-drain.model';
import { Boost } from 'src/app/model/osrs/boost.model';
import { CombatStats } from 'src/app/model/osrs/skill.type';
import { BoostService } from 'src/app/services/boost.service';
import { CombatStatService } from 'src/app/services/combat-stat.service';
import { StatDrainService } from 'src/app/services/stat-drain.service';

@Component({
  selector: 'app-gear-setup-settings',
  templateUrl: './gear-setup-settings.component.html',
  styleUrls: ['./gear-setup-settings.component.css'],
})
export class GearSetupSettingsComponent implements OnInit, OnDestroy {
  public gearSetupSettings: GearSetupSettings = {
    statDrains: null,
    boosts: null,
    combatStats: null,
  };

  private destroyed$ = new Subject();

  constructor(
    private boostService: BoostService,
    private statDrainService: StatDrainService,
    private combatStatService: CombatStatService
  ) {}

  ngOnDestroy(): void {
    this.destroyed$.next(true);
    this.destroyed$.complete();
  }

  ngOnInit(): void {
    this.boostService.globalBoosts$
      .pipe(takeUntil(this.destroyed$))
      .subscribe((boosts: Set<Boost>) => (this.gearSetupSettings.boosts = new Set(boosts)));

    this.statDrainService.globalStatDrain$
      .pipe(takeUntil(this.destroyed$))
      .subscribe((statDrains: StatDrain[]) => (this.gearSetupSettings.statDrains = [...statDrains]));

    this.combatStatService.globalCombatStats$
      .pipe(takeUntil(this.destroyed$))
      .subscribe((combatStats: CombatStats) => (this.gearSetupSettings.combatStats = { ...combatStats }));
  }

  toggleBoost(boost: Boost): void {
    this.boostService.toggleBoost(boost, this.gearSetupSettings.boosts);
  }

  statDrainsChanged(statDrains: StatDrain[]): void {
    this.gearSetupSettings.statDrains = statDrains;
  }

  combatStatsChanged(combatStats: CombatStats): void {
    this.gearSetupSettings.combatStats = { ...combatStats };
  }
}
