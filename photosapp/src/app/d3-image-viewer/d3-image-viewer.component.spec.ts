import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { D3ImageViewerComponent } from './d3-image-viewer.component';

describe('D3ImageViewerComponent', () => {
  let component: D3ImageViewerComponent;
  let fixture: ComponentFixture<D3ImageViewerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ D3ImageViewerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(D3ImageViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
