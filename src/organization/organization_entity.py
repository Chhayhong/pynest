from datetime import datetime
from sqlalchemy import Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.config import config

class Organization(config.Base):
    __tablename__ = "organization"

    organization_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True,index=True)
    description: Mapped[str] = mapped_column(String(512))
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(68))
    privacy: Mapped[str] = mapped_column(String, default="Private",index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
class AccountOrganization(config.Base):
    __tablename__ = 'account_organization'

    account_organization_id = mapped_column(Integer, primary_key=True)
    account_id = mapped_column(Integer, ForeignKey('account.account_id'))
    organization_id = mapped_column(Integer, ForeignKey('organization.organization_id',ondelete='CASCADE'))