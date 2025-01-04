import datetime

from src.config import config
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Attendee(config.Base):
    __tablename__ = 'attendee'

    attendee_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name:Mapped[str] = mapped_column(String(64))
    email:Mapped[str] = mapped_column(String(125)) #Will send confirmation email to this email
    phone_number = mapped_column(String(20))
    bio:Mapped[str] = mapped_column(String(255))
    remarks = mapped_column(String(255))
    profile_picture = mapped_column(String(255))


class AttendeeList(config.Base):
    __tablename__ = 'attendee_list'

    attendee_list_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id = mapped_column(Integer, ForeignKey('event.event_id'))
    account_id = mapped_column(Integer, ForeignKey('account.account_id'))
    attendee_id = mapped_column(Integer, ForeignKey('attendee.attendee_id', ondelete='CASCADE'), nullable=False)
    registration_time = mapped_column(DateTime, default=datetime.datetime.now())
    registration_status = mapped_column(String, default="Pending")


    