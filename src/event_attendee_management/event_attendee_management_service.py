import time

from ..event_management.event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import AccountOrganization as AccountOrganizationEntity
from .event_attendee_management_model import AttendeeRegister
from .event_attendee_management_entity import AttendeeList as EventAttendeeListEntity, Attendee as AttendeeEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventAttendeeManagementService:

    @async_db_request_handler
    async def add_event_attendee_management(self, event_id:int,account_id:int, event_attendee_register: AttendeeRegister, session: AsyncSession):
        async with session.begin():
            new_event_attendee = AttendeeEntity(
            **event_attendee_register.model_dump()
            )
            session.add(new_event_attendee)
            await session.flush()

            add_attendee_list = EventAttendeeListEntity(
            event_id=event_id, attendee_id=new_event_attendee.attendee_id, account_id=account_id
            )
            session.add(add_attendee_list)
        await session.commit()
        return new_event_attendee.attendee_id

    @async_db_request_handler
    async def get_managed_event_attendee_list(self, account_id: int, session: AsyncSession):
        query = select(AttendeeEntity).join(
            EventAttendeeListEntity, AttendeeEntity.attendee_id == EventAttendeeListEntity.attendee_id
        ).join(
            EventManagementEntity, EventAttendeeListEntity.event_id == EventManagementEntity.event_id
        ).join(
            AccountOrganizationEntity, AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id
        ).where(
            AccountOrganizationEntity.account_id == account_id,
            EventManagementEntity.event_id == EventAttendeeListEntity.event_id,
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def get_participated_event(self,account_id:int, session: AsyncSession):
        query = select(EventManagementEntity.name,AccountOrganizationEntity,EventAttendeeListEntity).where(
            EventAttendeeListEntity.account_id == account_id,
            AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id,
            EventAttendeeListEntity.event_id == EventManagementEntity.event_id)
        result = await session.execute(query)
        return result.scalars().all()
    
