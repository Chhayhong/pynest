from .event_management_model import EventManagement
from .event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import Organization as OrganizationEntity, AccountOrganization as AccountOrganizationEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventManagementService:

    @async_db_request_handler
    async def add_event_management(self,organization_id:int, event_management: EventManagement, session: AsyncSession):
        new_event_management = EventManagementEntity(
            **event_management.dict()
        )
        new_event_management.organization_id = organization_id
        new_event_management.start_time = new_event_management.start_time.replace(tzinfo=None)
        new_event_management.end_time = new_event_management.end_time.replace(tzinfo=None)
        session.add(new_event_management)
        await session.commit()
        return new_event_management.event_id

    @async_db_request_handler
    async def get_event_management(self, account_id: int, session: AsyncSession):
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
        )
        result = await session.execute(query)
        event_managements = []
        for event_management, organization in result.all():
            event_management_dict = event_management.__dict__
            event_management_dict['organization'] = organization.__dict__
            event_managements.append(event_management_dict)
        return event_managements
