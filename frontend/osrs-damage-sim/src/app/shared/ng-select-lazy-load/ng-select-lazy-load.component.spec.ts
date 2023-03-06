import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NgSelectLazyLoadComponent } from './ng-select-lazy-load.component';

describe('NgSelectLazyLoadComponent', () => {
  let component: NgSelectLazyLoadComponent;
  let fixture: ComponentFixture<NgSelectLazyLoadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NgSelectLazyLoadComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NgSelectLazyLoadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
