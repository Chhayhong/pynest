from fastapi import HTTPException
from nest.core import Controller, Get, Post, Depends,Patch
from sqlalchemy.ext.asyncio import AsyncSession

from ..annotation.max_limit_query import max_limit_query
from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from src.authorization_utils import get_current_account,Not_Authorized_Message
from src.config import config


from .event_attendee_management_service import EventAttendeeManagementService
from ..event_management.event_management_service import EventManagementService
from .event_attendee_management_model import AttendeeRegister, AttendeeUpdate


@Controller("v1/event_attendee", tag="Event attendee management")
class EventAttendeeManagementController:

    def __init__(self, event_attendee_management_service: EventAttendeeManagementService,event_management_service: EventManagementService):
        self.event_attendee_management_service = event_attendee_management_service
        self.event_management_service = event_management_service

    @Get("/participated")
    @handle_status_code_500_exceptions
    @max_limit_query()
    async def get_my_participated_event(self,limit:int=100,offset:int=0,session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_attendee_management_service.get_my_participated_event(current_account_id,session,limit,offset)

    @Post("/register/{event_id}")
    @handle_status_code_500_exceptions
    async def register_to_participate_in_event(self,event_id:int, event_attendee_register: AttendeeRegister, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        result = await self.event_attendee_management_service.check_attendee_already_joined_event(current_account_id, event_id, session)
        if result == "Event not found":
            raise HTTPException(status_code=404, detail="Event not found")
        if result == "Account joined this event":
            raise HTTPException(status_code=409, detail="This account has already registered for the event")
        result = await self.event_attendee_management_service.add_event_attendee_management(event_id, current_account_id, event_attendee_register, session)
        return result
    
    @Patch("/update/{event_id}/{attendee_id}")
    @handle_status_code_500_exceptions
    async def update_attendee_info(self, event_id:int,attendee_id:int,attendee:AttendeeUpdate, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        result = await self.event_attendee_management_service.update_attendee_info(event_id,attendee_id,current_account_id,attendee, session)
        if not result:
            raise HTTPException(status_code=404, detail="Event attendee not found")
        return result
 