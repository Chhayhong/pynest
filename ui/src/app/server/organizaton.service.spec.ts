import { TestBed } from '@angular/core/testing';

import { OrganizatonService } from './organizaton.service';

describe('OrganizatonService', () => {
  let service: OrganizatonService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(OrganizatonService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
