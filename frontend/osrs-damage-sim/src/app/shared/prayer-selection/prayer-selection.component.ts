import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { allPrayers, Prayer } from 'src/app/model/osrs/prayer.model';
import { PrayerModalComponent } from '../prayer-modal/prayer-modal.component';
import { disabledPrayers } from './disabled-prayers.const';

@Component({
  selector: 'app-prayer-selection',
  templateUrl: './prayer-selection.component.html',
  styleUrls: ['./prayer-selection.component.css'],
})
export class PrayerSelectionComponent implements OnInit, OnChanges {
  @Input()
  selectedPrayers: Set<Prayer>;

  @Input()
  quickPrayers: Set<Prayer> = new Set(['piety', 'chivalry', 'rigour', 'eagle_eye', 'augury', 'mystic_might']);

  @Output()
  prayerToggle = new EventEmitter<Prayer>();

  allPrayers = allPrayers;

  quickPrayerSelected = true;

  constructor(private modalService: NgbModal) {}
  ngOnChanges(): void {
    this.quickPrayerSelected = this.isOnlyQuickPrayerSelected();
  }

  ngOnInit(): void {
    this.quickPrayerSelected = this.isOnlyQuickPrayerSelected();
  }

  open() {
    const prayerModal = this.modalService.open(PrayerModalComponent, { animation: false });
    prayerModal.componentInstance.selectedPrayers = this.selectedPrayers;
    prayerModal.componentInstance.disabledPrayers = disabledPrayers;
    prayerModal.componentInstance.prayerToggle.subscribe((prayer: Prayer) => {
      this.togglePrayer(prayer);
    });
  }

  togglePrayer(prayer: Prayer): void {
    this.prayerToggle.emit(prayer);
    this.quickPrayerSelected = this.isOnlyQuickPrayerSelected();
  }

  isOnlyQuickPrayerSelected(): boolean {
    for (const selectedPrayer of this.selectedPrayers) {
      if (!this.quickPrayers.has(selectedPrayer)) {
        return false;
      }
    }
    return true;
  }
}
