from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field

from ..organization.organization_model import OrganizationResponse  # Ensure this import is correct and the Organization class is defined in the specified module


class EventManagementCreate(BaseModel):
    name: str
    description: str
    start_time: datetime 
    end_time: datetime
    location: str
    google_map: Optional[str]
    speaker: Optional[List[Union[str, dict]]] = Field(default_factory=list)
    sponsor: Optional[List[Union[str, dict]]] = Field(default_factory=list)
    partner: Optional[List[Union[str, dict]]] = Field(default_factory=list)
    status: str
    seat_limit: int
    event_setting: Optional[dict] = Field(default_factory=dict)
    event_type: str
    event_language: str

class EventManagementBaseModel(BaseModel):   
    name: str
    description: str
    start_time: datetime 
    end_time: datetime
    location: str
    google_map: Optional[str]
    speaker: Optional[List[Union[str, dict]]] = Field(default_factory=list)
    sponsor: Optional[List[Union[str, dict]]] = Field(default_factory=list)
    partner: Optional[List[Union[str, dict]]] = Field(default_factory=list)
    status: str
    seat_limit: int
    event_setting: Optional[dict] = Field(default_factory=dict)
    event_type: str
    event_language: str
    created_at: datetime
    updated_at: datetime
    privacy: str
    organization: OrganizationResponse
    

class EventManagementResponse(BaseModel):
    items: list[EventManagementBaseModel]
    previous: int
    next: int
    total: int


