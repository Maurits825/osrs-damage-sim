import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareInputSetupComponent } from './share-input-setup.component';

describe('ShareInputSetupComponent', () => {
  let component: ShareInputSetupComponent;
  let fixture: ComponentFixture<ShareInputSetupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShareInputSetupComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShareInputSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
