from typing import Optional
from fastapi import HTTPException
from nest.core import Controller, Get, Post, Depends,Patch
from sqlalchemy.ext.asyncio import AsyncSession

from ..annotation.max_limit_query import max_limit_query

from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from ..authorization_utils import get_current_account
from src.config import config
from ..authorization_utils import Not_Authorized_Message


from .event_management_service import EventManagementService
from .event_management_model import EventManagementCreate, EventManagementResponse, EventManagementUpdate


@Controller("v1/event_management", tag="Event management")
class EventManagementController:

    def __init__(self, event_management_service: EventManagementService):
        self.event_management_service = event_management_service

    @Get("/",response_model=EventManagementResponse)
    @handle_status_code_500_exceptions
    @max_limit_query()
    async def get_events_management(self,limit: Optional[int] = 100, offset: Optional[int] = 0, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_management_service.get_events_management(current_account_id,session,limit,offset)

    @Post("/{organization_id}/")
    @handle_status_code_500_exceptions
    async def add_event_management(self, organization_id:int,event_management: EventManagementCreate, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        is_account_owned_organization = await self.event_management_service.get_organization_account_owner(organization_id,current_account_id,session)
        if not is_account_owned_organization:
            raise HTTPException(status_code=403, detail=Not_Authorized_Message)
        return await self.event_management_service.add_event_management(organization_id,event_management, session)
    
    @Patch("/event/{event_id}")
    @handle_status_code_500_exceptions
    async def update_event_management(self, event_id:int,event_management: EventManagementUpdate, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        is_account_owned_event = await self.event_management_service.get_event_account_owner(event_id,current_account_id,session)
        if not is_account_owned_event:
            raise HTTPException(status_code=403, detail=Not_Authorized_Message)
        return await self.event_management_service.update_event_management(event_id,event_management, session)

 