from pydantic import BaseModel


class EventOrganizer(BaseModel):
    full_name: str
    email: str
    event_role: str = "General"
    detail: str
    profile_picture: str
    telegram_url: str
    facebook_url: str
    phone: str
