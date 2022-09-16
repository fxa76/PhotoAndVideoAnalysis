import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchParamComponent } from './search-param.component';

describe('SearchParamComponent', () => {
  let component: SearchParamComponent;
  let fixture: ComponentFixture<SearchParamComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchParamComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchParamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
