from fastapi import HTTPException
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..authorization_utils import get_current_account
from src.config import config


from .event_organizer_service import EventOrganizerService
from .event_organizer_model import EventOrganizer


@Controller("v1/event_organizer", tag="Event organizer")
class EventOrganizerController:

    def __init__(self, event_organizer_service: EventOrganizerService):
        self.event_organizer_service = event_organizer_service

    @Get("/")
    async def get_event_organizer(self, session: AsyncSession = Depends(config.get_db)):
        return await self.event_organizer_service.get_event_organizer(session)

    @Post("/{event_id}")
    async def add_event_organizer(self, event_id:int,event_organizer: EventOrganizer, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        result = await self.event_organizer_service.add_event_organizer(event_id,current_account_id,event_organizer, session)
        if result == "Event not found or does not belong to your account":
            raise HTTPException(status_code=404, detail=result)
        if result == "Duplicate full_name found for this event":
            raise HTTPException(status_code=409, detail=result)
        return result
 