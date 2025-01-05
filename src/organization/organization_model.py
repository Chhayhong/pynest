from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator
from typing_extensions import Self

class OrganizationCreate(BaseModel):
    name: str
    description: str
    address: str
    phone: str
   

class OrganizationResponse(BaseModel):
    organization_id: int
    name: str
    description: str
    address: str
    phone: str
    privacy:str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class OrganizationPaginations(BaseModel):
    items: list[OrganizationResponse]
    previous: int
    next: int
    total: int

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None 
    address: Optional[str] = None 
    phone: Optional[str] = None 
    privacy: Optional[str] = None
    
    @model_validator(mode='after')
    def check_privacy(self) -> Self:
        if self.privacy and self.privacy not in ['Public', 'Private']:
            raise ValueError('Privacy must be one of public or private')
        return self

class DeleteOrganization(BaseModel):
    detail: str = "Organization deleted successfully"

