from typing import Optional
from pydantic import BaseModel, EmailStr


class AttendeeRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    bio:str
    remarks: Optional[str] = None
    profile_picture: Optional[str] = None

class AttendeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None
    remarks: Optional[str] = None
    facebook: Optional[str] = None
    telegram: Optional[str] = None
    profile_picture: Optional[str] = None


class AttendeeListCreate(BaseModel):
    event_id: int
    account_id: int
    attendee_id: int
    registration_status: str = "Pending"

