import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CombatStatSelectionComponent } from './combat-stat-selection.component';

describe('CombatStatSelectionComponent', () => {
  let component: CombatStatSelectionComponent;
  let fixture: ComponentFixture<CombatStatSelectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CombatStatSelectionComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CombatStatSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
