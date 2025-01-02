from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..authorization_utils import get_current_account
from src.config import config


from .event_management_service import EventManagementService
from .event_management_model import EventManagement


@Controller("event_management", tag="event_management")
class EventManagementController:

    def __init__(self, event_management_service: EventManagementService):
        self.event_management_service = event_management_service

    @Get("/")
    async def get_event_management(self, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_management_service.get_event_management(current_account_id,session)

    @Post("/{organization_id}/")
    async def add_event_management(self, organization_id:int,event_management: EventManagement, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        return await self.event_management_service.add_event_management(organization_id,event_management, session)
 