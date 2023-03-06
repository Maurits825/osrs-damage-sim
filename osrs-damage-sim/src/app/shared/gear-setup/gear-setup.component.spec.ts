import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GearSetupComponent } from './gear-setup.component';

describe('GearSetupComponent', () => {
  let component: GearSetupComponent;
  let fixture: ComponentFixture<GearSetupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GearSetupComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(GearSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
