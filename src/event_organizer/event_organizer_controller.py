from typing import Optional
from fastapi import HTTPException
from nest.core import Controller, Get, Post, Depends,Patch
from sqlalchemy.ext.asyncio import AsyncSession
from ..authorization_utils import get_current_account,Not_Authorized_Message
from src.config import config


from .event_organizer_service import EventOrganizerService
from .event_organizer_model import EventOrganizer, EventOrganizerUpdate


@Controller("v1/event_organizer", tag="Event organizer")
class EventOrganizerController:

    def __init__(self, event_organizer_service: EventOrganizerService):
        self.event_organizer_service = event_organizer_service

    @Get("/")
    async def get_event_managed_organizers(self, limit:Optional[int]=100,offset:Optional[int]=0, session: AsyncSession = Depends(config.get_db), current_account_id: int = Depends(get_current_account), full_name: str = None):
        return await self.event_organizer_service.get_event_organizers(current_account_id, session,limit,offset,full_name)

    @Post("/{event_id}")
    async def add_event_organizer(self, event_id:int,event_organizer: EventOrganizer, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        result = await self.event_organizer_service.add_event_organizer_to_owned_organization(event_id,current_account_id,event_organizer, session)
        if result == "Event not found or does not belong to your account":
            raise HTTPException(status_code=404, detail=result)
        if result == "Duplicate full_name found for this event":
            raise HTTPException(status_code=409, detail=result)
        return result
    
    @Get("/{event_id}")
    async def get_event_organizer_by_event_id(self, event_id:int, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        is_account_owned_event = await self.event_organizer_service.check_account_owned_event(event_id,current_account_id,session)
        if not is_account_owned_event:
            return []
        return await self.event_organizer_service.get_event_organizer_by_event_id(event_id, session)
    
    @Patch("/{event_id}/{organizer_id}")
    async def update_event_organizer(self, event_id:int, organizer_id:int, event_organizer: EventOrganizerUpdate, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        result = await self.event_organizer_service.update_event_organizer(event_id, organizer_id, event_organizer, session)
        if not result:
            raise HTTPException(status_code=404, detail="Event organizer not found")
        return result
 