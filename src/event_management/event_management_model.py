from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from sqlalchemy import DateTime


class EventManagement(BaseModel):
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

