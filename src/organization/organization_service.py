from .organization_model import OrganizationCreate
from .organization_entity import Organization as OrganizationEntity, AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class OrganizationService:

    @async_db_request_handler
    async def add_organization(self,creator_account_id:int, organization: OrganizationCreate, session: AsyncSession):
        query = select(OrganizationEntity).where(OrganizationEntity.name == organization.name)
        existing_organization = await session.execute(query)
        if existing_organization.scalars().first():
            raise ValueError("Organization with the same name already exists.")
    
        new_organization = OrganizationEntity(
            **organization.model_dump()
        )
        session.add(new_organization)
        await session.flush()  # Ensure the new organization gets an ID

        account_organization = AccountOrganizationEntity(
            account_id=creator_account_id,
            organization_id=new_organization.organization_id
        )
        session.add(account_organization)
        session.add(new_organization)
        await session.commit()
        return new_organization.__dict__

    @async_db_request_handler
    async def get_organization(self, session: AsyncSession):
        query = select(OrganizationEntity)
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def get_organizations_by_account_id(self, account_id: int, session: AsyncSession):
        query = select(OrganizationEntity).join(AccountOrganizationEntity).where(AccountOrganizationEntity.account_id == account_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def update_organization(self, organization_id: int, account_id: int, organization_payload: OrganizationCreate, session: AsyncSession):
        organization_exist = await self.check_organization_exist(organization_id, session)
        if organization_exist is None:
            return None
        
        query = select(AccountOrganizationEntity).where(
            AccountOrganizationEntity.organization_id == int(organization_id),
            AccountOrganizationEntity.account_id == account_id
        )
        account_organization = await session.execute(query)
        if account_organization.scalars().one_or_none() is None:
            return None
        
        # Update the organization details
        organization_exist.name = organization_payload.name
        if hasattr(organization_payload, 'description'):
            organization_exist.description = organization_payload.description
        if hasattr(organization_payload, 'address'):
            organization_exist.address = organization_payload.address
        if hasattr(organization_payload, 'phone'):
            organization_exist.phone = organization_payload.phone
        
        await session.commit()
        return organization_exist

    @async_db_request_handler
    async def get_organization_by_name(self, organization_name: str, session: AsyncSession):
        query = select(OrganizationEntity).where(OrganizationEntity.name == organization_name)
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
    async def search_organization(self, organization_name: str, session: AsyncSession):
        query = select(OrganizationEntity).filter(OrganizationEntity.name.ilike(f'%{organization_name}%'))
        result = await session.execute(query)
        return result.scalars().all()
    
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