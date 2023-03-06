import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareInputSetupModalComponent } from './share-input-setup-modal.component';

describe('ShareInputSetupModalComponent', () => {
  let component: ShareInputSetupModalComponent;
  let fixture: ComponentFixture<ShareInputSetupModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShareInputSetupModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShareInputSetupModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
