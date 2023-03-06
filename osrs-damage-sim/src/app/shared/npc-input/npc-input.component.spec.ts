import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NpcInputComponent } from './npc-input.component';

describe('NpcInputComponent', () => {
  let component: NpcInputComponent;
  let fixture: ComponentFixture<NpcInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NpcInputComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(NpcInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
