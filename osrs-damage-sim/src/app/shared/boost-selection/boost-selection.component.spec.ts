import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoostSelectionComponent } from './boost-selection.component';

describe('BoostSelectionComponent', () => {
  let component: BoostSelectionComponent;
  let fixture: ComponentFixture<BoostSelectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BoostSelectionComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(BoostSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
