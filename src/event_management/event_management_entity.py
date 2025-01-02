from datetime import datetime
from src.config import config
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB



class EventManagement(config.Base):
    __tablename__ = "event"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organization_id = mapped_column(Integer, ForeignKey('organization.organization_id'))
    name = mapped_column(String,index=True)
    description = mapped_column(String)
    start_time = mapped_column(DateTime)
    end_time = mapped_column(DateTime)
    location = mapped_column(String)
    google_map = mapped_column(String)
    speaker = mapped_column(JSONB)
    sponsor = mapped_column(JSONB)
    partner = mapped_column(JSONB)
    status = mapped_column(String)
    seat_limit = mapped_column(Integer)
    event_setting = mapped_column(JSONB)
    event_type = mapped_column(String)
    event_language = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

