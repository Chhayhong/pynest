from .organization_model import OrganizationCreate
from .organization_entity import Organization as OrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class OrganizationService:

    @async_db_request_handler
    async def add_organization(self, organization: OrganizationCreate, session: AsyncSession):
        query = select(OrganizationEntity).where(OrganizationEntity.name == organization.name)
        existing_organization = await session.execute(query)
        if existing_organization.scalars().first():
            raise ValueError("Organization with the same name already exists.")
    
        new_organization = OrganizationEntity(
            **organization.model_dump()
        )
        session.add(new_organization)
        await session.commit()
        return new_organization.organization_id

    @async_db_request_handler
    async def get_organization(self, session: AsyncSession):
        query = select(OrganizationEntity)
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def update_organization(self, organization_id: int,organization_payload:OrganizationCreate, session: AsyncSession):
        organization =await self.check_organization_exist(organization_id,session)
        print(organization,"GGggggg")
        if organization is None:
            return None
        organization.name = organization_payload.name
        organization.description = organization_payload.description
        organization.address = organization_payload.address
        organization.phone = organization_payload.phone
        await session.commit()
        return organization

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
    async def delete_organization(self, organization_id: int, session: AsyncSession):
        query = delete(OrganizationEntity).where(OrganizationEntity.organization_id == int(organization_id))
        await session.execute(query)
        return await session.commit()
       
    
    @async_db_request_handler
    async def search_organization(self, organization_name: str, session: AsyncSession):
        query = select(OrganizationEntity).filter(OrganizationEntity.name.ilike(f'%{organization_name}%'))
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def get_organization_by_id(self, organization_id: int, session: AsyncSession):
        query = select(OrganizationEntity).where(OrganizationEntity.organization_id == organization_id)
        result = await session.execute(query)
        return result.scalars().one_or_none()