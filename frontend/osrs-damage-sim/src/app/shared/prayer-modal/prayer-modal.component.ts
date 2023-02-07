import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { allPrayers, Prayer } from 'src/app/model/osrs/prayer.model';

@Component({
  selector: 'app-prayer-modal',
  templateUrl: './prayer-modal.component.html',
  styleUrls: ['./prayer-modal.component.css'],
})
export class PrayerModalComponent implements OnInit {
  @Input()
  selectedPrayers: Set<Prayer>;

  @Output()
  prayerToggle = new EventEmitter<Prayer>();

  rows = Array(6)
    .fill(0)
    .map((_, i) => i);
  cols = Array(5)
    .fill(0)
    .map((_, i) => i);

  allPrayers = allPrayers;

  constructor(public activeModal: NgbActiveModal) {}

  ngOnInit(): void {}

  togglePrayer(prayer: Prayer): void {
    this.prayerToggle.emit(prayer);
  }
}
