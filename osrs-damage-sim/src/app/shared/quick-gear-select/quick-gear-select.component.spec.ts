import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuickGearSelectComponent } from './quick-gear-select.component';

describe('QuickGearSelectComponent', () => {
  let component: QuickGearSelectComponent;
  let fixture: ComponentFixture<QuickGearSelectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ QuickGearSelectComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuickGearSelectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
