import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TimelinebarComponent } from './timelinebar.component';

describe('TimelinebarComponent', () => {
  let component: TimelinebarComponent;
  let fixture: ComponentFixture<TimelinebarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TimelinebarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimelinebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
