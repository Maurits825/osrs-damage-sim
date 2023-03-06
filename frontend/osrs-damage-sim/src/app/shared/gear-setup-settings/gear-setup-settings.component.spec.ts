import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GearSetupSettingsComponent } from './gear-setup-settings.component';

describe('GearSetupSettingsComponent', () => {
  let component: GearSetupSettingsComponent;
  let fixture: ComponentFixture<GearSetupSettingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GearSetupSettingsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GearSetupSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
