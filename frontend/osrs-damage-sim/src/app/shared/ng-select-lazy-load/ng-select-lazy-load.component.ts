import { Component, ContentChild, EventEmitter, Input, OnDestroy, Output, TemplateRef } from '@angular/core';
import { Subject, distinctUntilChanged, takeUntil } from 'rxjs';

@Component({
  selector: 'app-ng-select-lazy-load',
  templateUrl: './ng-select-lazy-load.component.html',
  styleUrls: ['./ng-select-lazy-load.component.css'],
})
export class NgSelectLazyLoadComponent<T> implements OnDestroy {
  @Input()
  valueType: T;

  @Input()
  allValues: T[];

  @Input()
  searchProperty: string;

  @Input()
  placeholder: string;

  @ContentChild('dropdownLabel') dropdownLabel: TemplateRef<any>;
  @ContentChild('dropdownOptions') dropdownOptions: TemplateRef<any>;

  @Output()
  valueChanged = new EventEmitter<T>();

  valuesBuffer: T[];
  bufferSize = 50;
  numberOfItemsFromEndBeforeFetchingMore = 10;

  loading = false;
  input$ = new Subject<string>();

  private destroy$ = new Subject();

  constructor() {}

  ngOnInit(): void {
    this.valuesBuffer = this.allValues.slice(0, this.bufferSize);
    this.onSearch();
  }

  ngOnDestroy() {
    this.destroy$.next(null);
    this.destroy$.complete();
  }

  selectedValueChange(value: T): void {
    this.valueChanged.emit(value);
  }

  onScrollToEnd(searchTerm: string): void {
    this.fetchMore(searchTerm);
  }

  fetchMore(searchTerm: string): void {
    const len = this.valuesBuffer.length;
    const more = this.allValues
      .filter((value: T) => this.valueFilter(value, searchTerm))
      .slice(len, this.bufferSize + len);

    // TODO timeout is needed because otherwise the onScrollToEnd only triggers once, can maybe use OnScroll instead
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
      this.valuesBuffer = this.valuesBuffer.concat(more);
    }, 1);
  }

  onSearch(): void {
    this.input$.pipe(takeUntil(this.destroy$), distinctUntilChanged()).subscribe((searchTerm) => {
      this.valuesBuffer = this.allValues
        .filter((value: T) => this.valueFilter(value, searchTerm))
        .slice(0, this.bufferSize);
    });
  }

  valueFilter(value: T, searchTerm: string): boolean {
    if (!searchTerm) return true;
    return (value as any)[this.searchProperty].toLowerCase().includes(searchTerm.toLowerCase());
  }
}
