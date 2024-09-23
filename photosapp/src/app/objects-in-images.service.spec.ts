import { TestBed } from '@angular/core/testing';

import { ObjectsInImagesService } from './objects-in-images.service';

describe('ObjectsInImagesService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ObjectsInImagesService = TestBed.inject(ObjectsInImagesService);
    expect(service).toBeTruthy();
  });
});
