from .event_organizer_model import EventOrganizer
from .event_organizer_entity import EventOrganizer as EventOrganizerEntity
from ..event_management.event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventOrganizerService:

    @async_db_request_handler
    async def add_event_organizer(self, event_id: int, account_id: int, event_organizer: EventOrganizer, session: AsyncSession):
        existing_organizer_query = select(EventOrganizerEntity).where(
                EventOrganizerEntity.full_name == event_organizer.full_name,
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
            return new_event_organizer.organizer_id
        except Exception:
            await session.rollback()
            

    @async_db_request_handler
    async def get_event_organizer(self, session: AsyncSession):
        query = select(EventOrganizerEntity)
        result = await session.execute(query)
        return result.scalars().all()
