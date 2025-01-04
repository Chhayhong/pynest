from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from src.authorization_utils import get_current_account
from src.config import config


from .event_attendee_management_service import EventAttendeeManagementService
from .event_attendee_management_model import AttendeeRegister


@Controller("api/event_attendee", tag="Event attendee management")
class EventAttendeeManagementController:

    def __init__(self, event_attendee_management_service: EventAttendeeManagementService):
        self.event_attendee_management_service = event_attendee_management_service

    @Get("/")
    @handle_status_code_500_exceptions
    async def get_participated_event(self,session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_attendee_management_service.get_participated_event(current_account_id,session)

    @Post("/{event_id}")
    @handle_status_code_500_exceptions
    async def register_event_attendee(self,event_id:int, event_attendee_register: AttendeeRegister, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_attendee_management_service.add_event_attendee_management(event_id,current_account_id,event_attendee_register, session)
    
    @Get("/managed_list")
    @handle_status_code_500_exceptions
    async def get_managed_event_attendee_list(self, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_attendee_management_service.get_managed_event_attendee_list(current_account_id,session)
 