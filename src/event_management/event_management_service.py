from .event_management_model import EventManagement
from .event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import Organization as OrganizationEntity, AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventManagementService:

    @async_db_request_handler
    async def add_event_management(self,organization_id:int, event_management: EventManagement, session: AsyncSession):
        new_event_management = EventManagementEntity(
            **event_management.model_dump()
        )
        new_event_management.organization_id = organization_id
        new_event_management.start_time = new_event_management.start_time.replace(tzinfo=None)
        new_event_management.end_time = new_event_management.end_time.replace(tzinfo=None)
        session.add(new_event_management)
        await session.commit()
        return new_event_management.event_id

    @async_db_request_handler
    async def get_events_management(self, account_id: int, session: AsyncSession, limit: int = 100, offset: int = 0):
        query = select(
            EventManagementEntity,
            OrganizationEntity
        ).join(
            OrganizationEntity
        ).join(
            AccountOrganizationEntity
        ).where(
            EventManagementEntity.organization_id == OrganizationEntity.organization_id,
            AccountOrganizationEntity.account_id == account_id
        ).limit(limit).offset(offset)
        
        result = await session.execute(query)
        event_managements = []
        for event_management, organization in result.all():
            event_management_dict = event_management.__dict__
            event_management_dict['organization'] = organization.__dict__
            event_managements.append(event_management_dict)
        
        total_query = select(
            func.count(EventManagementEntity.event_id)
        ).select_from(
            EventManagementEntity
        ).join(
            OrganizationEntity
        ).join(
            AccountOrganizationEntity
        ).where(
            EventManagementEntity.organization_id == OrganizationEntity.organization_id,
            AccountOrganizationEntity.account_id == account_id
        )
        
        total_result = await session.execute(total_query)
        total = total_result.scalar_one()

        next_offset = (int(offset or 0) + int(limit or 0)) if (int(offset or 0) + int(limit or 0)) < int(total) else None
        previous_offset = (int(offset or 0) - int(limit or 0)) if (int(offset or 0) - int(limit or 0)) >= 0 else None

        return {
            "items": event_managements,
            "previous": int(previous_offset or 0),
            "next": int(next_offset or 0),
            "total": int(total or 0)
        }
    
    @async_db_request_handler
    async def get_organization_account_owner(self,organization_id:int,account_id:int,session:AsyncSession):
        query = select(
            AccountOrganizationEntity.organization_id
        ).where(
            AccountOrganizationEntity.account_id == account_id,
            AccountOrganizationEntity.organization_id == organization_id
        )
        result = await session.execute(query)
        return result.scalars().first()
    