import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpecialGearComponent } from './special-gear.component';

describe('SpecialGearComponent', () => {
  let component: SpecialGearComponent;
  let fixture: ComponentFixture<SpecialGearComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpecialGearComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpecialGearComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
