from src.config import config
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Users(config.Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String, unique=True, index=True)
    email = mapped_column(String, unique=True)
    password = mapped_column(String)
    role = mapped_column(String, default="user")
    refresh_token = mapped_column(String)


