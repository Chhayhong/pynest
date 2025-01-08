import { Component, inject } from '@angular/core';
import { OrganizatonService } from '../organizaton.service';
import { OrganizationInterface } from '../organization';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  organizationService = inject(OrganizatonService);

  organizations: OrganizationInterface | null = null;

  ngOnInit(): void {
    this.organizationService.getOrganizations().subscribe((response)=>{
      this.organizations = response
    })
  }
}
