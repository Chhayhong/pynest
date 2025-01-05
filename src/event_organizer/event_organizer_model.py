from pydantic import BaseModel
from typing import Optional


class EventOrganizer(BaseModel):
    full_name: str
    email: str
    event_role: str = "General"
    detail: str
    profile_picture: str
    telegram_url: str
    facebook_url: str
    phone: str

class EventOrganizerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    event_role: Optional[str] = None
    detail: Optional[str] = None
    profile_picture: Optional[str] = None
    telegram_url: Optional[str] = None
    facebook_url: Optional[str] = None
    phone: Optional[str] = None