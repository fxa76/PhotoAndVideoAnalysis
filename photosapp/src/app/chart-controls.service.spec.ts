import { TestBed } from '@angular/core/testing';

import { ChartControlsService } from './chart-controls.service';

describe('ChartControlsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ChartControlsService = TestBed.inject(ChartControlsService);
    expect(service).toBeTruthy();
  });
});
