import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Npc } from '../../model/osrs/npc.model';
import { DamageSimService } from '../../services/damage-sim.service';

@Component({
  selector: 'app-npc-input',
  templateUrl: './npc-input.component.html',
  styleUrls: ['./npc-input.component.css'],
})
export class NpcInputComponent implements OnInit {
  @Input()
  selectedNpc: Npc;

  @Output()
  npcChanged = new EventEmitter<Npc>();

  allNpcs: Npc[];

  Npc: Npc; //TODO do this properly ...

  constructor(private damageSimservice: DamageSimService) {}

  ngOnInit(): void {
    this.damageSimservice.allNpcs$.subscribe((allNpcs: Npc[]) => {
      this.allNpcs = allNpcs;
    });
  }

  selectedNpcChange(npc: Npc): void {
    this.npcChanged.emit(npc);
  }
}
