from fastapi import HTTPException
from ..event_management.event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import AccountOrganization as AccountOrganizationEntity
from .event_attendee_management_model import AttendeeRegister
from .event_attendee_management_entity import AttendeeList as EventAttendeeListEntity, Attendee as AttendeeEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EventAttendeeManagementService:

    @async_db_request_handler
    async def add_event_attendee_management(self, event_id:int,account_id:int, event_attendee_register: AttendeeRegister, session: AsyncSession):
        try:
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
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
       
    @async_db_request_handler
    async def check_attendee_already_joined_event(self,account_id:int, event_id: int, session: AsyncSession):
        event_query = select(EventManagementEntity).where(EventManagementEntity.event_id == event_id)
        event_result = await session.execute(event_query)
        event = event_result.scalars().first()

        if not event:
            return "Event not found"
        existing_attendee_query = select(EventAttendeeListEntity).where(
                EventAttendeeListEntity.event_id == event_id,
                EventAttendeeListEntity.account_id == account_id
            )
        existing_attendee_result = await session.execute(existing_attendee_query)
        existing_attendee = existing_attendee_result.scalars().first()

        if existing_attendee:
            return "Account joined this event"
        return True

    @async_db_request_handler
    async def get_managed_event_attendee_list(self, account_id: int, session: AsyncSession, limit: int = 100, offset: int = 0):
        query = select(
            EventManagementEntity.event_id,
            EventManagementEntity.name,
            AttendeeEntity
        ).join(
            EventAttendeeListEntity, AttendeeEntity.attendee_id == EventAttendeeListEntity.attendee_id
        ).join(
            EventManagementEntity, EventAttendeeListEntity.event_id == EventManagementEntity.event_id
        ).join(
            AccountOrganizationEntity, AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id
        ).where(
            AccountOrganizationEntity.account_id == account_id,
            EventManagementEntity.event_id == EventAttendeeListEntity.event_id,
        ).group_by(
            EventManagementEntity.event_id,
            EventManagementEntity.name,
            AttendeeEntity.attendee_id
        ).limit(limit).offset(offset)
        
        result = await session.execute(query)
        attendees_by_event = {}
        for event_id, name, attendee in (result.all() or []):
            if event_id not in attendees_by_event:
                attendees_by_event[event_id] = {
                    "name": name,
                    "event_id": event_id,
                    "attendees": []
                }
            attendees_by_event[event_id]["attendees"].append(attendee)
        
        total_query = select(func.count()).select_from(
            EventAttendeeListEntity
        ).join(
            EventManagementEntity, EventAttendeeListEntity.event_id == EventManagementEntity.event_id
        ).join(
            AccountOrganizationEntity, AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id
        ).where(
            AccountOrganizationEntity.account_id == account_id
        )
        total_result = await session.execute(total_query)
        total = total_result.scalar()

        previous_offset = offset - limit if offset - limit >= 0 else None
        next_offset = offset + limit if offset + limit < total else None

        return {
            "items": attendees_by_event,
            "previous": int(previous_offset or 0),
            "next": int(next_offset or 0),
            "total": int(total or 0)
        }
       
    @async_db_request_handler
    async def get_my_participated_event(self,account_id:int, session: AsyncSession, limit: int = 100, offset: int = 0):
        query = select(EventManagementEntity,AccountOrganizationEntity,EventAttendeeListEntity).where(
            EventAttendeeListEntity.account_id == account_id,
            AccountOrganizationEntity.organization_id == EventManagementEntity.organization_id,
            EventAttendeeListEntity.event_id == EventManagementEntity.event_id)
        result = await session.execute(query)
        total_query = select(func.count()).select_from(
            EventAttendeeListEntity
        ).where(
            EventAttendeeListEntity.account_id == account_id
        )
        total_result = await session.execute(total_query)
        total = total_result.scalar()

        previous_offset = offset - limit if offset - limit >= 0 else None
        next_offset = offset + limit if offset + limit < total else None

        return {
            "items": result.scalars().all(),
            "previous": int(previous_offset or 0),
            "next": int(next_offset or 0),
            "total": int(total or 0)
        }
    
