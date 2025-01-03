from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from nest.core.decorators.database import async_db_request_handler

from .account_model import AccountUpdateStatus
from .account_entity import Account as AccountEntity
from sqlalchemy import func, select
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@Injectable
class AdminAccountService:
     
    @async_db_request_handler
    async def get_accounts(self,session: AsyncSession,limit:int,offset:int):
        query = select(AccountEntity).offset(offset).limit(limit)
        result = await session.execute(query)
        accounts = result.scalars().all()
        total = await session.execute(select(func.count()).select_from(AccountEntity))
        total = total.scalar()
        previous_offset = offset - limit if offset - limit >= 0 else None
        next_offset = offset + limit if offset + limit < total else None

        return {
            "items": accounts,
            "previous": int(previous_offset or 0),
            "next": int(next_offset or 0),
            "total": int(total or 0)
        }
        
    
    @async_db_request_handler
    async def get_account(self, account_id: int, session: AsyncSession):
        query = select(AccountEntity).where(
        AccountEntity.account_id == int(account_id),
        )
        result = await session.execute(query)
        return result.scalars().first()
    
    @async_db_request_handler
    async def update_account(self, account_id: int, updated_account: AccountUpdateStatus, session: AsyncSession):
        query = select(AccountEntity).where(
            AccountEntity.account_id == int(account_id),
        )
        result = await session.execute(query)
        account = result.scalars().first()
        if account:
            account.is_active = bool(updated_account.is_active)
            await session.commit()
        return account
    