import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GearSetupTabsComponent } from './gear-setup-tabs.component';

describe('GearSetupTabsComponent', () => {
  let component: GearSetupTabsComponent;
  let fixture: ComponentFixture<GearSetupTabsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GearSetupTabsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(GearSetupTabsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
