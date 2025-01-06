from typing import Optional

from ..utils import calculate_offsets
from .organization_model import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from .organization_entity import Organization as OrganizationEntity, AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class OrganizationService:

    @async_db_request_handler
    async def add_organization(self,creator_account_id:int, organization: OrganizationCreate, session: AsyncSession):
        new_organization = OrganizationEntity(
            **organization.model_dump()
        )
        session.add(new_organization)
        await session.flush()
        
        account_organization = AccountOrganizationEntity(
            organization_id=new_organization.organization_id,
            account_id=creator_account_id
        )
        session.add(account_organization)
        await session.commit()
        return new_organization

    @async_db_request_handler
    async def get_organizations_public(self, session: AsyncSession, limit: int = 100, offset: int = 0, name: Optional[str] = None):
        query = select(OrganizationEntity).where(OrganizationEntity.privacy == "Public")
        if name is not None:
            query = query.where(OrganizationEntity.name.ilike(f'%{name}%'))
        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        organizations = result.scalars().all()

        total_query = select(func.count()).select_from(OrganizationEntity).where(OrganizationEntity.privacy == "Public")
        if name is not None:
            total_query = total_query.where(OrganizationEntity.name.ilike(f'%{name}%'))
        total_result = await session.execute(total_query)
        total = total_result.scalar()
        next_offset, previous_offset = calculate_offsets(offset, limit, total)

        return {
            "items": organizations,
            "previous": previous_offset,
            "next": next_offset,
            "total": total
        }
    
    @async_db_request_handler
    async def get_owned_organizations(self, account_id: int, session: AsyncSession, limit: int = 100, offset: int = 0, name: Optional[str] = None):
        query = select(OrganizationEntity).join(AccountOrganizationEntity).where(AccountOrganizationEntity.account_id == account_id)
        if name is not None:
            query = query.where(OrganizationEntity.name.ilike(f'%{name}%'))
        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        organizations = result.scalars().all()

        total_query = select(func.count()).select_from(OrganizationEntity).join(AccountOrganizationEntity).where(AccountOrganizationEntity.account_id == account_id)
        if name is not None:
            total_query = total_query.where(OrganizationEntity.name.ilike(f'%{name}%'))
        total_result = await session.execute(total_query)
        total = total_result.scalar()
        next_offset, previous_offset = calculate_offsets(offset, limit, total)

        return {
            "items": organizations,
            "previous": previous_offset,
            "next": next_offset,
            "total": total
        }
    
    @async_db_request_handler
    async def update_organization(self, organization_id: int, account_id: int, organization: OrganizationUpdate, session: AsyncSession):
        organization_exist:OrganizationResponse = await self.check_organization_exist(organization_id, session)
        if organization_exist is None:
            return None
        
        query = select(AccountOrganizationEntity).where(
            AccountOrganizationEntity.organization_id == int(organization_id),
            AccountOrganizationEntity.account_id == account_id
        )
        account_organization = await session.execute(query)
        if account_organization.scalars().one_or_none() is None:
            return None
        
        for key, value in organization.model_dump().items():
            if value is not None:  # Only update fields that are not None
                setattr(organization_exist, key, value)
        
        await session.commit()
        return organization_exist.organization_id

    @async_db_request_handler
    async def get_exist_organization_by_name(self, organization_name: str,account_id:int, session: AsyncSession):
        query = select(OrganizationEntity).join(AccountOrganizationEntity).where(
            OrganizationEntity.name == organization_name,
            AccountOrganizationEntity.account_id == account_id
            )
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @async_db_request_handler
    async def check_organization_exist(self, organization_id: int, session: AsyncSession):
        query = select(OrganizationEntity).where(
        OrganizationEntity.organization_id == int(organization_id))
        result = await session. execute(query)
        return result.scalars().one_or_none()
    
    @async_db_request_handler
    async def delete_organization(self, organization_id: int, account_id: int, session: AsyncSession):
        # Check if the account is associated with the organization
        query = select(AccountOrganizationEntity).where(
            AccountOrganizationEntity.organization_id == organization_id,
            AccountOrganizationEntity.account_id == account_id
        )
        account_organization = await session.execute(query)
        if account_organization.scalars().one_or_none() is None:
            return False
        
        # Delete related records in AccountOrganizationEntity
        delete_account_organization_query = delete(AccountOrganizationEntity).where(
            AccountOrganizationEntity.organization_id == organization_id
        )
        await session.execute(delete_account_organization_query)
        
        # Delete the organization
        delete_query = delete(OrganizationEntity).where(OrganizationEntity.organization_id == organization_id)
        await session.execute(delete_query)
        await session.commit()
       
    @async_db_request_handler
    async def search_organization_by_account_id(self, account_id: int, organization_name: str, session: AsyncSession):
        query = select(OrganizationEntity).join(AccountOrganizationEntity).where(
            AccountOrganizationEntity.account_id == account_id,
            OrganizationEntity.name.ilike(f'%{organization_name}%')
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def get_organization_by_id(self, organization_id: int, session: AsyncSession):
        query = select(OrganizationEntity).where(OrganizationEntity.organization_id == organization_id)
        result = await session.execute(query)
        return result.scalars().one_or_none()
    