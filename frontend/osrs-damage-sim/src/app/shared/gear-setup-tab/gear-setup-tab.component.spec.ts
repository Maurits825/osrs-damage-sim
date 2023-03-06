import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GearSetupTabComponent } from './gear-setup-tab.component';

describe('GearSetupTabComponent', () => {
  let component: GearSetupTabComponent;
  let fixture: ComponentFixture<GearSetupTabComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GearSetupTabComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(GearSetupTabComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
