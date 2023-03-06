import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimResultsComponent } from './sim-results.component';

describe('SimResultsComponent', () => {
  let component: SimResultsComponent;
  let fixture: ComponentFixture<SimResultsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SimResultsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SimResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
