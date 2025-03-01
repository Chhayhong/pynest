import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { OrganizationInterface } from './organization';

@Injectable({
  providedIn: 'root'
})
export class OrganizatonService {
API = "http://localhost:8000/v1/public/organizations"

  constructor(
    private readonly http: HttpClient
  ) { }

  getOrganizations() {
    return this.http.get<OrganizationInterface>(this.API);
  }
}
