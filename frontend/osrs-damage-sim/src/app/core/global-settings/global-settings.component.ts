import { Component, OnDestroy, OnInit } from '@angular/core';
import { Boost } from '../../model/osrs/boost.model';
import { GlobalSettings, InputSetup } from '../../model/damage-sim/input-setup.model';
import { Npc } from '../../model/osrs/npc.model';
import { BoostService } from '../../services/boost.service';
import { Prayer } from 'src/app/model/osrs/prayer.model';
import { allAttackTypes, AttackType } from 'src/app/model/osrs/item.model';
import { PrayerService } from 'src/app/services/prayer.service';
import { CombatStats } from 'src/app/model/osrs/skill.type';
import { CombatStatService } from 'src/app/services/combat-stat.service';
import { StatDrain } from 'src/app/model/damage-sim/stat-drain.model';
import { StatDrainService } from 'src/app/services/stat-drain.service';
import { TOA_NPCS, TOA_PATH_LVL_NPCS } from 'src/app/shared/components/npc-input/npc.const';
import { InputSetupService } from 'src/app/services/input-setup.service';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-global-settings',
  templateUrl: './global-settings.component.html',
  styleUrls: ['./global-settings.component.css'],
})
export class GlobalSettingsComponent implements OnInit, OnDestroy {
  globalSettings: GlobalSettings = {
    npc: null,
    iterations: 10000,
    teamSize: 1,
    raidLevel: 0,
    pathLevel: 0,
    isDetailedRun: false,
  };

  showPathLevel = false;
  showRaidLevel = false;

  selectedBoosts: Set<Boost> = new Set();

  allAttackTypes = allAttackTypes;

  selectedPrayers: Record<AttackType, Set<Prayer>> = {
    magic: new Set(['augury']),
    melee: new Set(['piety']),
    ranged: new Set(['rigour']),
  };

  quickPrayers: Record<AttackType, Set<Prayer>> = {
    magic: new Set(['augury']),
    melee: new Set(['piety']),
    ranged: new Set(['rigour']),
  };

  combatStats: CombatStats = {
    attack: 99,
    strength: 99,
    ranged: 99,
    magic: 99,
    hitpoints: 99,
  };

  statDrains: StatDrain[] = [];

  loading = false;

  private destroyed$ = new Subject();

  constructor(
    private boostService: BoostService,
    private prayerService: PrayerService,
    private combatStatService: CombatStatService,
    private statDrainService: StatDrainService,
    private inputSetupService: InputSetupService
  ) {}

  ngOnInit(): void {
    this.prayerService.globalPrayers$.next(this.selectedPrayers);
    this.inputSetupService.loadInputSetup$
      .pipe(takeUntil(this.destroyed$))
      .subscribe((inputSetup: InputSetup) => this.setGlobalSettings(inputSetup.globalSettings));

    this.inputSetupService.globalSettingsComponent$.next(this);
  }

  ngOnDestroy(): void {
    this.destroyed$.next(true);
    this.destroyed$.complete();
  }

  setGlobalSettings(globalSettings: GlobalSettings): void {
    this.globalSettings = globalSettings;
    this.npcChanged(this.globalSettings.npc);
  }

  npcChanged(npc: Npc): void {
    this.globalSettings.npc = npc;

    if (!npc) return;

    const npcName = npc.name;
    this.showPathLevel = false;
    this.showRaidLevel = false;

    if (TOA_PATH_LVL_NPCS.includes(npcName)) {
      this.showPathLevel = true;
      this.showRaidLevel = true;
    } else if (TOA_NPCS.includes(npcName)) {
      this.showRaidLevel = true;
      this.globalSettings.pathLevel = 0;
    } else {
      this.globalSettings.raidLevel = 0;
      this.globalSettings.pathLevel = 0;
    }
  }

  toggleBoost(boost: Boost): void {
    this.boostService.toggleBoost(boost, this.selectedBoosts);
    this.boostService.globalBoosts$.next(this.selectedBoosts);
  }

  toggleAttackTypePrayer(prayer: Prayer, attackType: AttackType): void {
    this.prayerService.togglePrayer(prayer, this.selectedPrayers[attackType]);
    this.prayerService.globalPrayers$.next(this.selectedPrayers);
  }

  combatStatsChanged(combatStats: CombatStats): void {
    this.combatStatService.globalCombatStats$.next(combatStats);
  }

  statDrainChanged(statDrains: StatDrain[]): void {
    this.statDrainService.globalStatDrain$.next(statDrains);
  }

  onDetailedRunChanged(isDetailedRun: boolean): void {
    if (isDetailedRun) {
      this.globalSettings.iterations = Math.min(5000, this.globalSettings.iterations);
    }
  }
}
