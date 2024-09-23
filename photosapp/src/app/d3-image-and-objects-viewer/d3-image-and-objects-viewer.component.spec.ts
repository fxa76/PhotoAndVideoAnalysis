import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { D3ImageAndObjectsViewerComponent } from './d3-image-and-objects-viewer.component';

describe('D3ImageAndObjectsViewerComponent', () => {
  let component: D3ImageAndObjectsViewerComponent;
  let fixture: ComponentFixture<D3ImageAndObjectsViewerComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ D3ImageAndObjectsViewerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(D3ImageAndObjectsViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
