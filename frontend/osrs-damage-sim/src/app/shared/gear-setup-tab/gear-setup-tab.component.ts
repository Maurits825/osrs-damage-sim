import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  ComponentRef,
  Inject,
  Injector,
  Input,
  Optional,
  SkipSelf,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import { cloneDeep } from 'lodash-es';
import { GEAR_SETUP_TOKEN, INPUT_GEAR_SETUP_TOKEN } from 'src/app/model/damage-sim/injection-token.const';
import { GearSetup, GearSetupSettings, InputGearSetup } from 'src/app/model/damage-sim/input-setup.model';
import { GearSetupSettingsComponent } from '../gear-setup-settings/gear-setup-settings.component';
import { GearSetupComponent } from '../gear-setup/gear-setup.component';

@Component({
  selector: 'app-gear-setup-tab',
  templateUrl: './gear-setup-tab.component.html',
  styleUrls: ['./gear-setup-tab.component.css'],
})
export class GearSetupTabComponent implements AfterViewInit {
  @Input() active = false;

  @ViewChild('gearSetupsContainer', { read: ViewContainerRef }) gearSetupsContainer: ViewContainerRef;
  @ViewChild(GearSetupSettingsComponent) gearSetupSettingsComponent: GearSetupSettingsComponent;

  id = 0;
  gearSetups: ComponentRef<GearSetupComponent>[] = [];

  constructor(
    private changeDetector: ChangeDetectorRef,
    @SkipSelf() @Optional() @Inject(INPUT_GEAR_SETUP_TOKEN) public inputGearSetupToCopy: InputGearSetup
  ) {}

  public ngAfterViewInit(): void {
    if (this.inputGearSetupToCopy) {
      this.gearSetupSettingsComponent.gearSetupSettings = cloneDeep(this.inputGearSetupToCopy.gearSetupSettings);

      this.addNewGearSetup(this.inputGearSetupToCopy.mainGearSetup, true);
      this.inputGearSetupToCopy.fillGearSetups.forEach((gearSetup: GearSetup) => {
        this.addNewGearSetup(gearSetup);
      });
    } else {
      this.addNewGearSetup(null, true);
    }

    this.changeDetector.detectChanges();
  }

  addNewGearSetup(gearSetup?: GearSetup, isMainGearSetup = false): void {
    let gearSetupRef;

    if (gearSetup) {
      const injector: Injector = Injector.create({
        providers: [{ provide: GEAR_SETUP_TOKEN, useValue: gearSetup }],
      });
      gearSetupRef = this.gearSetupsContainer.createComponent(GearSetupComponent, { injector: injector });
    } else {
      gearSetupRef = this.gearSetupsContainer.createComponent(GearSetupComponent);
    }

    gearSetupRef.instance.setupCount = this.gearSetups.length + 1;
    gearSetupRef.instance.isMainGearSetup = isMainGearSetup;
    gearSetupRef.instance.gearSetupTabRef = this;

    this.gearSetups.push(gearSetupRef);
  }

  removeGearSetup(id: number): void {
    const gearSetupRef = this.gearSetups.find((setup) => setup.instance.setupCount == id);

    const gearSetupsContainerIndex: number = this.gearSetupsContainer.indexOf(gearSetupRef.hostView);

    this.gearSetupsContainer.remove(gearSetupsContainerIndex);

    this.gearSetups = this.gearSetups.filter((setup) => setup.instance.setupCount !== id);

    for (let index = 0; index < this.gearSetups.length; index++) {
      this.gearSetups[index].instance.setupCount = index + 1;
    }
  }

  getGearSetupSettings(): GearSetupSettings {
    return this.gearSetupSettingsComponent.gearSetupSettings;
  }
}
