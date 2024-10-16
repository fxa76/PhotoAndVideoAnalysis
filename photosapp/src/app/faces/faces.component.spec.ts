import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { FacesComponent } from './faces.component';

describe('FacesComponent', () => {
  let component: FacesComponent;
  let fixture: ComponentFixture<FacesComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ FacesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FacesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
