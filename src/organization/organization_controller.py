from typing import List, Optional
from fastapi import HTTPException
from nest.core import Controller, Get, Post, Depends,Patch
from sqlalchemy.ext.asyncio import AsyncSession

from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from ..authorization_utils import get_current_account
from src.config import config


from .organization_service import OrganizationService
from .organization_model import DeleteOrganization, OrganizationCreate, OrganizationPaginations, OrganizationUpdate


@Controller("v1/organization", tag="Organization management")
class OrganizationController:

    def __init__(self, organization_service: OrganizationService):
        self.organization_service = organization_service

    @Get("/organizations/{limit=100}/{offset=0}", response_model=OrganizationPaginations)
    @handle_status_code_500_exceptions
    async def get_owned_organizations(self,limit: Optional[int] = 100, offset: Optional[int] = 0, session: AsyncSession = Depends(config.get_db), current_account_id: int = Depends(get_current_account), name: Optional[str] = None):
        return await self.organization_service.get_owned_organizations(current_account_id, session,limit,offset, name)
    
    # @Get("/{organization_id}")

    @Post("/register", response_model=OrganizationCreate)
    @handle_status_code_500_exceptions
    async def add_organization(self, organization: OrganizationCreate, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        existing_organization = await self.organization_service.get_exist_organization_by_name(organization.name, session)
        if existing_organization:
            raise HTTPException(status_code=409, detail="Organization with the same name already exists")
        return await self.organization_service.add_organization(current_account_id,organization, session)
    
    
    @Patch("/update", response_model=OrganizationUpdate)
    @handle_status_code_500_exceptions
    async def update_organization(self, organization_id:str, organization: OrganizationUpdate, session:AsyncSession=Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        result = await self.organization_service.update_organization(organization_id,current_account_id, organization, session)
        if result is None:
            raise HTTPException(status_code=404, detail="Organization not found")
        return result
    
    @Post("/delete", response_model=DeleteOrganization)
    @handle_status_code_500_exceptions
    async def delete_organization(self, organization_id: int, session: AsyncSession=Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        organization = await self.organization_service.get_organization_by_id(organization_id, session)
        if organization is None:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        is_failed = await self.organization_service.delete_organization(organization_id,current_account_id, session)
        if is_failed:
            raise HTTPException(status_code=500, detail="Failed to delete organization")
        
        return {"detail": "Organization deleted successfully"}

    