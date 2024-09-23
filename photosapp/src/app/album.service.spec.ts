import { TestBed } from '@angular/core/testing';

import { AlbumService } from './album.service';

describe('AlbumService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: AlbumService = TestBed.inject(AlbumService);
    expect(service).toBeTruthy();
  });
});
