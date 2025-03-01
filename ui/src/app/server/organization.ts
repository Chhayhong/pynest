export interface OrganizationInterface{
    items: Organization[]
    previous: number
    next: number
    total: number
  }
  
  export interface Organization {
    name: string
    organization_id: number
    description: string
    phone: string
    verified: boolean
    created_at: string
    address: string
    privacy: string
    origanization_url: any
    updated_at: string
  }
  