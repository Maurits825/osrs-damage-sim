import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrayerSelectionComponent } from './prayer-selection.component';

describe('PrayerSelectionComponent', () => {
  let component: PrayerSelectionComponent;
  let fixture: ComponentFixture<PrayerSelectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PrayerSelectionComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrayerSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
