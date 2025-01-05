from typing import Optional
from nest.core import Controller
from nest.core import Controller, Get, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..organization.organization_service import OrganizationService

from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from src.config import config
from ..annotation.max_limit_query import max_limit_query

@Controller("v1/public/organizations", tag="Organization public")
class OrganizationPublicController:
    def __init__(self, organization_service: OrganizationService):
        self.organization_service = organization_service
    
    @Get("/")
    @handle_status_code_500_exceptions
    @max_limit_query()
    async def get_organizations(self, session: AsyncSession = Depends(config.get_db),limit:Optional[int]=100,offset:Optional[int]=0, name: Optional[str] = None):
        return await self.organization_service.get_organizations_public(session,limit,offset,name)
    