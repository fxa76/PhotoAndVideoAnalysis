import { TestBed } from '@angular/core/testing';

import { SearchParamService } from './search-param.service';

describe('SearchParamService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SearchParamService = TestBed.inject(SearchParamService);
    expect(service).toBeTruthy();
  });
});
