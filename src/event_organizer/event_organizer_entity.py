from src.config import config
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class EventOrganizer(config.Base):
    __tablename__ = "organizer"

    organizer_id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name:Mapped[str] = mapped_column(String(64),unique=True,index=True)
    email = mapped_column(String(64))
    event_role = mapped_column(String(120),default="General")
    detail = mapped_column(String(255))
    profile_picture = mapped_column(String(255))
    telegram_url = mapped_column(String(255))
    facebook_url = mapped_column(String(255))
    phone = mapped_column(String(64))
    event_id:Mapped[int] = mapped_column(Integer, ForeignKey('event.event_id'), nullable=False) 
    account_id = mapped_column(Integer, ForeignKey('account.account_id'), nullable=True)  #Create invite email to join organization

