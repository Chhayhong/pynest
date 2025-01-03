from typing import Optional
from fastapi import HTTPException
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..authorization_utils import get_current_account
from src.config import config


from .event_management_service import EventManagementService
from .event_management_model import EventManagement


@Controller("event_management", tag="Event management")
class EventManagementController:

    def __init__(self, event_management_service: EventManagementService):
        self.event_management_service = event_management_service

    @Get("/{limit=100}/{offset=0}")
    async def get_events_management(self,limit: Optional[int] = 100, offset: Optional[int] = 0, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_management_service.get_events_management(current_account_id,session,limit,offset)

    @Post("/{organization_id}/")
    async def add_event_management(self, organization_id:int,event_management: EventManagement, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        is_account_owned_organization = await self.event_management_service.get_organization_account_owner(organization_id,current_account_id,session)
        if not is_account_owned_organization:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return await self.event_management_service.add_event_management(organization_id,event_management, session)

 