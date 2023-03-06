import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-share-input-setup-modal',
  templateUrl: './share-input-setup-modal.component.html',
  styleUrls: ['./share-input-setup-modal.component.css'],
})
export class ShareInputSetupModalComponent {
  @Input()
  setupString: string;

  @Input()
  isValidSetup: boolean;

  @Output()
  copySetupToClipboard = new EventEmitter();

  @Output()
  loadSetup = new EventEmitter<string>();

  constructor(public activeModal: NgbActiveModal) {}

  onCopySetupToClipboard(): void {
    this.copySetupToClipboard.emit();
  }

  onLoadSetup(setupString: string): void {
    this.loadSetup.emit(setupString);
  }
}
