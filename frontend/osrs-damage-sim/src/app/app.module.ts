import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { NgSelectModule } from '@ng-select/ng-select';
import { AppComponent } from './app.component';
import { GearSetupComponent } from './gear-setup/gear-setup.component';
import { GeneralSetupComponent } from './general-setup/general-setup.component';
import { WikiItemIconPipe } from './pipes/wiki-item-icon.pipe';
import { DamageSimService } from './services/damage-sim.service';
import { GearSetupService } from './services/gear-setups.service';
import { RlGearService } from './services/rl-gear.service';

@NgModule({
  declarations: [
    AppComponent,
    GearSetupComponent,
    WikiItemIconPipe,
    GeneralSetupComponent,
  ],
  imports: [
    NgSelectModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserModule,
    HttpClientModule,
  ],
  providers: [
    DamageSimService,
    RlGearService,
    GearSetupService,
  ],
  bootstrap: [
    AppComponent,
    GearSetupComponent,
    GeneralSetupComponent,
  ]
})
export class AppModule { }
