from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.config import config
from src.users.users_entity import Users

class Organization(config.Base):
    __tablename__ = "organization"

    organization_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True,index=True)
    description: Mapped[str] = mapped_column(String(512))
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(68))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
