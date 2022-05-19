import { TestBed } from '@angular/core/testing';

import { CheckImagesService } from './check-images.service';

describe('CheckImagesService', () => {
  let service: CheckImagesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CheckImagesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
