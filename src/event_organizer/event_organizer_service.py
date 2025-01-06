import logging
from typing import Optional
from .event_organizer_model import EventOrganizer, EventOrganizerUpdate
from .event_organizer_entity import EventOrganizer as EventOrganizerEntity
from ..event_management.event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventOrganizerService:

    @async_db_request_handler
    async def add_event_organizer_to_owned_organization(self, event_id: int, account_id: int, event_organizer: EventOrganizer, session: AsyncSession):
        existing_organizer_query = select(EventOrganizerEntity).where(
                EventOrganizerEntity.full_name == event_organizer.full_name
                and
                EventOrganizerEntity.event_id == event_id
            )
        existing_organizer_result = await session.execute(existing_organizer_query)
        existing_organizer = existing_organizer_result.scalars().first()
        if existing_organizer:
            return "Duplicate full_name found for this event"
        event_query = select(EventManagementEntity).select_from(EventManagementEntity).join(AccountOrganizationEntity, AccountOrganizationEntity.account_id == account_id).where(
            EventManagementEntity.event_id == event_id,
            AccountOrganizationEntity.account_id == account_id
        )
        event_result = await session.execute(event_query)
        event = event_result.scalars().first()
        if not event:
            return "Event not found or does not belong to your account"
        
        new_event_organizer = EventOrganizerEntity(
            **event_organizer.model_dump()
        )
        new_event_organizer.event_id = event_id
        try:
            session.add(new_event_organizer)
            await session.commit()
            return new_event_organizer
        except Exception as e:
            await session.rollback()
            logging.error("Error creating event organizer: ", e)
            
            

    @async_db_request_handler
    async def get_event_organizers(self, account_id: int, session: AsyncSession, limit: Optional[int] = 100, offset: Optional[int] = 0, full_name: Optional[str] = None):
        query = select(EventOrganizerEntity).select_from(EventOrganizerEntity).join(EventManagementEntity, EventManagementEntity.event_id == EventOrganizerEntity.event_id).join(AccountOrganizationEntity, AccountOrganizationEntity.account_id == account_id).where(
            AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id,
            AccountOrganizationEntity.account_id == account_id
        )
        if full_name:
            query = query.where(EventOrganizerEntity.full_name.ilike(f"%{full_name}%"))
        
        query = query.limit(limit).offset(offset)
        
        total_query = select(func.count(EventOrganizerEntity.organizer_id)).select_from(EventOrganizerEntity).join(
            EventManagementEntity, EventManagementEntity.event_id == EventOrganizerEntity.event_id).join(
            AccountOrganizationEntity, AccountOrganizationEntity.account_id == account_id).where(
            AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id,
            AccountOrganizationEntity.account_id == account_id
        )
        if full_name:
            total_query = total_query.where(EventOrganizerEntity.full_name.ilike(f"%{full_name}%"))
        
        total_result = await session.execute(total_query)
        total = total_result.scalar()
        
        result = await session.execute(query)
        items = result.scalars().all()
        
        return {
            "items": items,
            "previous": offset | 0,
            "next": offset | 0 + limit | 0 if offset | 0 + limit | 0 < total else 0,
            "total": total
        }
    
    
    @async_db_request_handler
    async def get_event_organizer_by_event_id(self, event_id: int, session: AsyncSession):
        query = select(EventOrganizerEntity).where(EventOrganizerEntity.event_id == event_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def update_event_organizer(self, event_id: int, organizer_id: int, event_organizer: EventOrganizerUpdate, session: AsyncSession):
        query = select(EventOrganizerEntity).where(
            EventOrganizerEntity.event_id == event_id,
            EventOrganizerEntity.organizer_id == organizer_id
        )
        result = await session.execute(query)
        organizer = result.scalars().first()
        if not organizer:
            return False
        
        for key, value in event_organizer.model_dump().items():
            if value is not None:
                setattr(organizer, key, value)
        
        session.add(organizer)
        await session.commit()
        return organizer.organizer_id
    
    @async_db_request_handler
    async def check_account_owned_event(self, event_id: int, account_id: int, session: AsyncSession):
        query = select(EventManagementEntity, AccountOrganizationEntity).join(
            AccountOrganizationEntity, AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id
        ).where(
            EventManagementEntity.event_id == event_id,
            AccountOrganizationEntity.account_id == account_id
        )
        result = await session.execute(query)
        event = result.scalars().first()
        if not event:
            return False
        return True


