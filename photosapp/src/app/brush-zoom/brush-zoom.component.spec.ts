import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { BrushZoomComponent } from './brush-zoom.component';

describe('BrushZoomComponent', () => {
  let component: BrushZoomComponent;
  let fixture: ComponentFixture<BrushZoomComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ BrushZoomComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BrushZoomComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
