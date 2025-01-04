from typing import List, Optional
from fastapi import Depends, HTTPException
from nest.core import Controller
from nest.core import Controller, Get, Depends, Post
from ..annotation.max_limit_query import max_limit_query
from ..annotation.http_status_code_500_exception import handle_status_code_500_exceptions
from .admin_account_service import AdminAccountService
from .account_model import AccountResponseModelWithPaginations, AccountUpdateStatus, AccountsResponse
from ..authorization_utils import get_current_account,Not_Authorized_Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config

@Controller("v1/admin_account", tag="Admin account management")
class AdminAccountController:
    def __init__(self, admin_account_service:AdminAccountService):
        self.admin_account_service = admin_account_service

    @Get("/{limit=100}/{offset=0}", response_model=AccountResponseModelWithPaginations)
    @handle_status_code_500_exceptions
    @max_limit_query()
    async def get_accounts(self,limit: Optional[int] = 100, offset: Optional[int] = 0, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        authorized_account:AccountsResponse = await self.admin_account_service.get_account(current_account_id, session)
        if authorized_account.role != "admin":
            raise HTTPException(status_code=403, detail=Not_Authorized_Message)
        accounts = await self.admin_account_service.get_accounts(session,limit,offset)
        return accounts
    
    @Get("/{account_id}", response_model=AccountsResponse)
    @handle_status_code_500_exceptions
    async def get_account(self, account_id: int, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        authorized_account:AccountsResponse = await self.admin_account_service.get_account(current_account_id, session)
        if authorized_account.role != "admin":
            raise HTTPException(status_code=403, detail=Not_Authorized_Message)
        account = await self.admin_account_service.get_account(account_id, session)
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return account
    
    @Post("/{account_id}",response_model=AccountsResponse)
    @handle_status_code_500_exceptions
    async def update_account_status(self, account_id: int, updated_account: AccountUpdateStatus, session: AsyncSession = Depends(config.get_db),current_account_id: int = Depends(get_current_account)):
        authorized_account:AccountsResponse = await self.admin_account_service.get_account(current_account_id, session)
        if authorized_account.role != "admin":
            raise HTTPException(status_code=403, detail=Not_Authorized_Message)
        account:AccountUpdateStatus = await self.admin_account_service.get_account(account_id, session)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        updated_account = await self.admin_account_service.update_account(account_id, updated_account, session)
        return updated_account
    

