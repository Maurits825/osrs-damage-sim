import { Component, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ClipboardService } from 'ngx-clipboard';
import { InputSetupService } from 'src/app/services/input-setup.service';
import { ShareInputSetupModalComponent } from 'src/app/shared/share-input-setup-modal/share-input-setup-modal.component';
import { GearSetupTabsComponent } from '../gear-setup-tabs/gear-setup-tabs.component';
import { GlobalSettingsComponent } from '../global-settings/global-settings.component';

@Component({
  selector: 'app-share-input-setup',
  templateUrl: './share-input-setup.component.html',
  styleUrls: ['./share-input-setup.component.css'],
})
export class ShareInputSetupComponent {
  @Input() globalSettingsComponent: GlobalSettingsComponent;
  @Input() gearSetupTabsComponent: GearSetupTabsComponent;

  setupString: string;

  constructor(
    private modalService: NgbModal,
    private inputSetupService: InputSetupService,
    private clipboardService: ClipboardService
  ) {}

  getSetupString(): string {
    const inputSetupJson = this.inputSetupService.getInputSetupAsJson(
      this.globalSettingsComponent.globalSettings,
      this.gearSetupTabsComponent
    );

    return window.btoa(inputSetupJson);
  }

  openModal() {
    const shareSetupModal = this.modalService.open(ShareInputSetupModalComponent, { animation: false });

    this.setupString = this.getSetupString();
    shareSetupModal.componentInstance.setupString = this.setupString;

    shareSetupModal.componentInstance.loadSetup.subscribe((setup: string) => {
      const isValidSetup = this.loadSetup(setup);
      shareSetupModal.componentInstance.isValidSetup = isValidSetup;
    });

    shareSetupModal.componentInstance.copySetupToClipboard.subscribe(() => {
      this.copySetupToClipboard();
    });
  }

  loadSetup(setup: string): boolean {
    if (!setup) return false;

    try {
      const inputSetupJson = window.atob(setup);
      const inputSetup = this.inputSetupService.parseInputSetup(inputSetupJson);

      this.gearSetupTabsComponent.loadInputSetup(inputSetup);
      this.globalSettingsComponent.setGlobalSettings(inputSetup.globalSettings);
    } catch (error) {
      return false;
    }

    return true;
  }

  copySetupToClipboard(): void {
    this.clipboardService.copy(this.setupString);
  }
}
