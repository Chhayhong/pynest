from datetime import datetime
from src.config import config
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB



class EventManagement(config.Base):
    __tablename__ = "event"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey('organization.organization_id'))
    name:Mapped[str] = mapped_column(String,index=True)
    description = mapped_column(String)
    start_time:Mapped[datetime] = mapped_column(DateTime)
    end_time:Mapped[datetime] = mapped_column(DateTime)
    location:Mapped[str] = mapped_column(String)
    google_map = mapped_column(String)
    speaker = mapped_column(JSONB)
    sponsor = mapped_column(JSONB)
    partner = mapped_column(JSONB)
    status = mapped_column(String,default="draft",index=True)
    privacy = mapped_column(String,default="Private",index=True)
    seat_limit:Mapped[int] = mapped_column(Integer,default=0)
    event_setting = mapped_column(JSONB)
    event_type = mapped_column(String,default="Offline",index=True)
    event_language = mapped_column(String,default="Khmer",index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

class EventManagementBasicCreate(config.Base):
    __tablename__ = "event"
    __table_args__ = {'extend_existing': True}
    name: Mapped[str]
    description: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    location: Mapped[str]
    google_map: Mapped[str]
    status: Mapped[str] = mapped_column(default="draft")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
