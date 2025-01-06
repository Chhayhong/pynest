from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator
from typing_extensions import Self

from src.shared_message_utils import PRIVACY_VALUE_ERROR_MESSAGE

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
    privacy:str = "Private"
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
            raise ValueError(PRIVACY_VALUE_ERROR_MESSAGE)
        return self
