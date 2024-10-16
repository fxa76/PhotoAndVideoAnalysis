import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ImageOverlayComponent } from './image-overlay.component';

describe('ImageOverlayComponent', () => {
  let component: ImageOverlayComponent;
  let fixture: ComponentFixture<ImageOverlayComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ImageOverlayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageOverlayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
