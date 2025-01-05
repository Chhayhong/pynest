from typing import Optional
from .event_management_model import EventManagementCreate, EventManagementUpdate
from .event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import Organization as OrganizationEntity, AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventManagementService:

    @async_db_request_handler
    async def add_event_management(self,organization_id:int, event_management: EventManagementCreate, session: AsyncSession):
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
    
    @async_db_request_handler
    async def get_public_events(self, session: AsyncSession, limit: int = 100, offset: int = 0,name:Optional[str] = None):
        query = select(EventManagementEntity).where(
            EventManagementEntity.privacy == "Public"
        )
        if name:
            query = query.where(EventManagementEntity.name.ilike(f"%{name}%"))
        query.limit(limit).offset(offset)
        result = await session.execute(query)
        event_managements = result.scalars().all()
        
        total_query = select(func.count(EventManagementEntity.event_id)).where(
            EventManagementEntity.privacy == "Public"
        )
        if name:
            total_query = total_query.where(EventManagementEntity.name.ilike(f"%{name}%"))
        total_result = await session.execute(total_query)
        total = total_result.scalar_one()

        next_offset = (int(offset or 0) + int(limit or 0)) if (int(offset or 0) + int(limit or 0)) < int(total) else None
        previous_offset = (int(offset or 0) - int(limit or 0)) if (int(offset or 0) - int(limit or 0)) >= 0 else None

        return {
            "items": [event_management.__dict__ for event_management in event_managements],
            "previous": int(previous_offset or 0),
            "next": int(next_offset or 0),
            "total": int(total or 0)
        }
    
    @async_db_request_handler
    async def update_event_management(self, event_id: int, event_management: EventManagementUpdate, session: AsyncSession):
        query = select(EventManagementEntity).where(EventManagementEntity.event_id == event_id)
        result = await session.execute(query)
        event = result.scalars().first()
        if not event:
            return False
        
        for key, value in event_management.model_dump().items():
            if value is not None:
                if key in ['start_time', 'end_time'] and value.tzinfo is not None:
                    value = value.replace(tzinfo=None)
                setattr(event, key, value)
        
        session.add(event)
        await session.commit()
        return event.event_id
    
    @async_db_request_handler
    async def get_event_account_owner(self,event_id:int,account_id:int,session:AsyncSession):
        query = select(
            EventManagementEntity.organization_id
        ).select_from(
            EventManagementEntity
        ).join(
            AccountOrganizationEntity,
            EventManagementEntity.organization_id == AccountOrganizationEntity.organization_id
        ).where(
            EventManagementEntity.event_id == event_id,
            AccountOrganizationEntity.account_id == account_id
        )
        result = await session.execute(query)
        return result.scalars().first()
    