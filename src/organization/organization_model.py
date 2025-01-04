from datetime import datetime
from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    name: str
    description: str
    address: str
    phone: str
    privacy: str

class OrganizationResponse(BaseModel):
    organization_id: int
    name: str
    description: str
    address: str
    phone: str
    privacy:str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class OrganizationUpdate(BaseModel):
    name: str 
    description: str 
    address: str 
    phone: str 
    privacy: str

class DeleteOrganization(BaseModel):
    detail: str = "Organization deleted successfully"

