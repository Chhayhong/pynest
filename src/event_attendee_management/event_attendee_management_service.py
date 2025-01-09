import logging
from fastapi import HTTPException
from sqlalchemy.orm._orm_constructors import aliased

from ..utils import calculate_offsets
from ..event_management.event_management_entity import EventManagement as EventManagementEntity
from ..organization.organization_entity import AccountOrganization as AccountOrganizationEntity
from .event_attendee_management_model import AttendeeRegister, AttendeeUpdate
from .event_attendee_management_entity import AttendeeList as EventAttendeeListEntity, Attendee as AttendeeEntity
from ..account.account_entity import Account as AccountEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import func, select,text
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
    async def get_managed_attendee_list_by_owned_event(self, account_id: int,event_id,  session: AsyncSession, limit: int = 100, offset: int = 0):
        sql = text("""
            SELECT a.*, atl.registration_status, atl.registration_time
            FROM attendee a
            JOIN attendee_list atl ON a.attendee_id = atl.attendee_id
            JOIN event e ON atl.event_id = e.event_id
            JOIN account_organization ao ON e.organization_id = ao.organization_id
            JOIN account acc ON ao.account_id = acc.account_id
            WHERE atl.event_id = :event_id AND acc.account_id = :account_id
            LIMIT :limit OFFSET :offset
        """)

        result = await session.execute(sql, {"event_id": event_id, "account_id": account_id, "limit": limit, "offset": offset})

        attendees = [
            dict(row._mapping) for row in result.fetchall()
        ]

        count_sql = text("""
            SELECT COUNT(*) 
            FROM attendee a
            JOIN attendee_list atl ON a.attendee_id = atl.attendee_id
            JOIN event e ON atl.event_id = e.event_id
            JOIN account_organization ao ON e.organization_id = ao.organization_id
            JOIN account acc ON ao.account_id = acc.account_id
            WHERE atl.event_id = :event_id AND acc.account_id = :account_id
        """)

        count_result = await session.execute(count_sql, {"event_id": event_id, "account_id": account_id})
        total = count_result.scalar()
        next_offset, previous_offset = calculate_offsets(offset, limit, total)

        return {
            "items": attendees,
            "previous": previous_offset,
            "next": next_offset,
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
        next_offset, previous_offset = calculate_offsets(offset, limit, total)

        return {
            "items": result.scalars().all(),
            "previous": previous_offset,
            "next": next_offset,
            "total": int(total or 0)
        }

    @async_db_request_handler 
    async def update_attendee_info(
        self,
        event_id: int,
        attendee_id: int,
        account_id: int,
        attendee: AttendeeUpdate,
        session: AsyncSession
    ):
        attendee_list_query = select(EventAttendeeListEntity).where(
            EventAttendeeListEntity.attendee_id == attendee_id,
            EventAttendeeListEntity.account_id == account_id,
            EventAttendeeListEntity.event_id == event_id
        )
        attendee_list_result = await session.execute(attendee_list_query)
        attendee_list_entry = attendee_list_result.scalars().first()
    
        if not attendee_list_entry:
            return False
    
        query = select(AttendeeEntity).where(AttendeeEntity.attendee_id == attendee_id)
        result = await session.execute(query)
        existing_attendee = result.scalars().first()
    
        if not existing_attendee:
            return False
    
        for key, value in attendee.model_dump().items():
            if value is not None:
                setattr(existing_attendee, key, value)
    
        # Start a new transaction if none is already active
        if not session.is_active:
            await session.begin()
    
        await session.commit()  # Commit within the transaction
        
        return existing_attendee.attendee_id
        
    @async_db_request_handler
    async def verify_registration_status(self, event_id: int, attendee_id: int,registration_status:str, session: AsyncSession):
        event_query = select(EventManagementEntity).where(EventManagementEntity.event_id == event_id)
        event_result = await session.execute(event_query)
        event = event_result.scalars().first()

        if not event:
            return "Event not found"

        attendee_query = select(AttendeeEntity).where(AttendeeEntity.attendee_id == attendee_id)
        attendee_result = await session.execute(attendee_query)
        attendee = attendee_result.scalars().first()

        if not attendee:
            return "Attendee not found"

        attendee_list_query = select(EventAttendeeListEntity).where(
            EventAttendeeListEntity.event_id == event_id,
            EventAttendeeListEntity.attendee_id == attendee_id
        )
        attendee_list_result = await session.execute(attendee_list_query)
        attendee_list_entry = attendee_list_result.scalars().first()

        if not attendee_list_entry:
            return "Attendee not registered for this event"

        attendee_list_entry.registration_status = registration_status
        await session.commit()
        return attendee_list_entry.attendee_id
    

            
        
