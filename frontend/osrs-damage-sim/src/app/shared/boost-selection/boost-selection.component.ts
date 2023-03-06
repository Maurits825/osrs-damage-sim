import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { allBoosts, Boost } from '../../model/osrs/boost.model';
import { BoostModalComponent } from '../boost-modal/boost-modal.component';

@Component({
  selector: 'app-boost-selection',
  templateUrl: './boost-selection.component.html',
  styleUrls: ['./boost-selection.component.css'],
})
export class BoostSelectionComponent implements OnInit, OnChanges {
  @Input()
  selectedBoosts: Set<Boost>;

  @Output()
  boostToggle = new EventEmitter<Boost>();

  allBoosts = allBoosts;
  quickBoosts: Set<Boost> = new Set(['overload_plus', 'smelling_salts', 'super_combat', 'ranging', 'saturated_heart']);
  quickBoostSelected = true;

  constructor(private modalService: NgbModal) {}

  ngOnChanges(): void {
    this.quickBoostSelected = this.isOnlyQuickBoostSelected();
  }

  ngOnInit(): void {
    this.quickBoostSelected = this.isOnlyQuickBoostSelected();
  }

  open() {
    const boostModal = this.modalService.open(BoostModalComponent, { animation: false });
    boostModal.componentInstance.selectedBoosts = this.selectedBoosts;
    boostModal.componentInstance.boostToggle.subscribe((boost: Boost) => {
      this.toggleBoost(boost);
    });
  }

  toggleBoost(boost: Boost): void {
    this.boostToggle.emit(boost);
    this.quickBoostSelected = this.isOnlyQuickBoostSelected();
  }

  isOnlyQuickBoostSelected(): boolean {
    for (const selectedBoost of this.selectedBoosts) {
      if (!this.quickBoosts.has(selectedBoost)) {
        return false;
      }
    }
    return true;
  }
}
