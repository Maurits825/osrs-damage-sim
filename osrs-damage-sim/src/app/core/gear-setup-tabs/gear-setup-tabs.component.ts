import { AfterViewInit, ChangeDetectorRef, Component, Injector, ViewChild, ViewContainerRef } from '@angular/core';
import { INPUT_GEAR_SETUP_TOKEN } from 'src/app/model/damage-sim/injection-token.const';
import { InputGearSetup, InputSetup } from 'src/app/model/damage-sim/input-setup.model';
import { InputSetupService } from 'src/app/services/input-setup.service';
import { GearSetupTabComponent } from '../../shared/gear-setup-tab/gear-setup-tab.component';

@Component({
  selector: 'app-gear-setup-tabs',
  templateUrl: './gear-setup-tabs.component.html',
  styleUrls: ['./gear-setup-tabs.component.css'],
})
export class GearSetupTabsComponent implements AfterViewInit {
  @ViewChild('gearSetupTabContainer', { read: ViewContainerRef }) gearSetupTabContainer: ViewContainerRef;
  gearSetupTabs: GearSetupTabComponent[] = [];

  constructor(private changeDetector: ChangeDetectorRef, private inputSetupService: InputSetupService) {}

  ngAfterViewInit(): void {
    this.openNewSetupTab();
    this.changeDetector.detectChanges();
  }

  openNewSetupTab(inputGearSetupToCopy?: InputGearSetup): void {
    let gearSetupTabRef;

    if (inputGearSetupToCopy) {
      const injector: Injector = Injector.create({
        providers: [{ provide: INPUT_GEAR_SETUP_TOKEN, useValue: inputGearSetupToCopy }],
      });
      gearSetupTabRef = this.gearSetupTabContainer.createComponent(GearSetupTabComponent, { injector: injector });
    } else {
      gearSetupTabRef = this.gearSetupTabContainer.createComponent(GearSetupTabComponent);
    }

    const tabInstance: GearSetupTabComponent = gearSetupTabRef.instance as GearSetupTabComponent;
    tabInstance.id = this.gearSetupTabs.length + 1;

    this.gearSetupTabs.push(tabInstance);

    this.selectTab(tabInstance);
  }

  selectTab(tab: GearSetupTabComponent): void {
    this.gearSetupTabs.forEach((gearSetupTab) => (gearSetupTab.active = false));

    tab.active = true;
  }

  closeTab(tab: GearSetupTabComponent): void {
    for (let i = 0; i < this.gearSetupTabs.length; i++) {
      if (this.gearSetupTabs[i] === tab) {
        this.gearSetupTabs.splice(i, 1);

        this.gearSetupTabContainer.remove(i);

        if (tab.active && this.gearSetupTabs.length >= 1) {
          const index = i == 0 ? i : i - 1;
          this.selectTab(this.gearSetupTabs[index]);
          break;
        }
      }
    }

    for (let index = 0; index < this.gearSetupTabs.length; index++) {
      this.gearSetupTabs[index].id = index + 1;
    }
  }

  copyTab(tabToCopy: GearSetupTabComponent): void {
    this.openNewSetupTab(this.inputSetupService.getGearInputSetup(tabToCopy));
  }

  loadInputSetup(inputSetup: InputSetup): void {
    for (let index = 0; index < this.gearSetupTabs.length; index++) {
      this.gearSetupTabContainer.remove();
    }

    this.gearSetupTabs.length = 0;

    inputSetup.inputGearSetups.forEach((inputGearSetup: InputGearSetup) => {
      this.openNewSetupTab(inputGearSetup);
    });
  }
}
