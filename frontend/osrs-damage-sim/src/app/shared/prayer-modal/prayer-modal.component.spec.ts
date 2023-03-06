import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrayerModalComponent } from './prayer-modal.component';

describe('PrayerModalComponent', () => {
  let component: PrayerModalComponent;
  let fixture: ComponentFixture<PrayerModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PrayerModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrayerModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
