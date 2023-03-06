import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoostModalComponent } from './boost-modal.component';

describe('BoostModalComponent', () => {
  let component: BoostModalComponent;
  let fixture: ComponentFixture<BoostModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoostModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BoostModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
