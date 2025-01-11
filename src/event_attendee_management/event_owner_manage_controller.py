from nest.core import Controller
from fastapi import HTTPException
from nest.core import Controller, Get, Depends,Patch
from sqlalchemy.ext.asyncio import AsyncSession

from ..event_management.event_management_service import EventManagementService

from ..event_attendee_management.event_attendee_management_service import EventAttendeeManagementService

from ..annotation.max_limit_query import max_limit_query
from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from src.authorization_utils import get_current_account,Not_Authorized_Message
from src.config import config

@Controller("event_owner_manage", tag="Event owner manage attendee")
class EventOwnerManageController:
    def __init__(self, event_attendee_management_service: EventAttendeeManagementService,event_management_service: EventManagementService):
        self.event_attendee_management_service = event_attendee_management_service
        self.event_management_service = event_management_service
    @Get("/managed_participant_list")
    @handle_status_code_500_exceptions
    @max_limit_query()
    async def get_managed_participant_attendee_list(self ,event_id:int,limit: int=100, offset: int=0, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_attendee_management_service.get_managed_attendee_list_by_owned_event(current_account_id,event_id,session,limit,offset)
    
    @Patch("/approve/registration_status/{event_id}/{attendee_id}")
    @handle_status_code_500_exceptions
    async def approve_attendee_registration_status(self, event_id:int,attendee_id:int,registration_status:str, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        check_owned_event = await self.event_management_service.get_event_account_owner(event_id,current_account_id,session)
        if not check_owned_event:
            raise HTTPException(status_code=403, detail=Not_Authorized_Message)
        result = await self.event_attendee_management_service.verify_registration_status(event_id,attendee_id,registration_status, session)
        if not result:
            raise HTTPException(status_code=404, detail="Event attendee not found")
        return result

    