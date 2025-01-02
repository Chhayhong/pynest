from src.config import config
from sqlalchemy import Integer, String,Boolean
from sqlalchemy.orm import Mapped, mapped_column


class Account(config.Base):
    __tablename__ = "account"

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String, unique=True, index=True,nullable=False)
    email = mapped_column(String, unique=True,nullable=True)
    password = mapped_column(String(255), nullable=False)
    role = mapped_column(String(64), default="user")
    refresh_token = mapped_column(String)
    is_active = mapped_column(Boolean, default=False)


