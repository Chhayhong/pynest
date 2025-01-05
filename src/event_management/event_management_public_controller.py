from nest.core import Controller
from typing import Optional
from fastapi import HTTPException
from nest.core import Controller, Get, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..annotation.max_limit_query import max_limit_query

from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from src.config import config


from .event_management_service import EventManagementService


@Controller("v1/public", tag="Public Events")
class EventManagementPublicController:
    def __init__(self, event_management_service: EventManagementService):
        self.event_management_service = event_management_service

    @Get("/events")
    @handle_status_code_500_exceptions
    @max_limit_query()
    async def get_public_events(self,limit: Optional[int] = 100, offset: Optional[int] = 0, session: AsyncSession = Depends(config.get_db),name: Optional[str] = None):
        return await self.event_management_service.get_public_events(session,limit,offset,name)
    