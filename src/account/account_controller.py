from fastapi import HTTPException
from typing import List
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config


from .account_service import AccountService
from .account_model import Account, AccountCreate, Token as TokenModel
from fastapi.security import OAuth2PasswordRequestForm


@Controller("v1/account", tag="Account management")
class AccountController:

    def __init__(self, account: AccountService):
        self.account = account

    @Post("/")
    async def register(self, account: AccountCreate, session: AsyncSession = Depends(config.get_db)):
        account_exist = await self.account.check_account_exist(account, session)
        if account_exist:
            raise HTTPException(status_code=409, detail="Account already exists")
        new_account = await self.account.add_account(account, session)
        return new_account
    
    @Post("/token", response_model=TokenModel)
    async def login_for_token(self, account:OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(config.get_db)):
        account_exist = await self.account.check_account_exist(account, session)
        if not account_exist:
            raise HTTPException(status_code=401, detail="Account does not exist")
        if not self.account.verify_password(account.password, account_exist.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = self.account.create_access_token({"sub": account.username,"role":account_exist.role,"account_id":str(account_exist.account_id)})
        refresh_token = await self.account.generate_refresh_token(account_exist.username, session)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
    
    @Get("/me", response_model=Account)
    async def get_current_account(self, token: str, session: AsyncSession = Depends(config.get_db)):
        username = self.account.verify_token(token)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
        
        account = await self.account.check_username_exist(username, session)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return account
    
    @Post("/logout")
    async def logout(self, token: str, session: AsyncSession = Depends(config.get_db)):
        username = self.account.verify_token(token)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
        
        account = await self.account.check_username_exist(username, session)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        
        account.refresh_token = None
        await session.commit()
        return {"detail": "Logged out successfully"}
        