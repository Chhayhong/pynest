from pydantic import BaseModel, EmailStr


class AttendeeRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    bio: str

class AttendeeListCreate(BaseModel):
    event_id: int
    account_id: int
    attendee_id: int
    registration_status: str = "Pending"

