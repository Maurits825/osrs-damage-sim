import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { allBoosts, Boost } from 'src/app/model/osrs/boost.model';
import { gridBoosts } from './boost-grid.const';

@Component({
  selector: 'app-boost-modal',
  templateUrl: './boost-modal.component.html',
  styleUrls: ['./boost-modal.component.css'],
})
export class BoostModalComponent {
  @Input()
  selectedBoosts: Set<Boost>;

  @Output()
  boostToggle = new EventEmitter<Boost>();

  gridBoosts = gridBoosts;
  allBoosts = allBoosts;

  boostCategoryIcons: string[] = ['attack', 'strength', 'combat', 'ranged', 'magic', 'vial'];

  constructor(public activeModal: NgbActiveModal) {}

  toggleBoost(boost: Boost): void {
    this.boostToggle.emit(boost);
  }
}
