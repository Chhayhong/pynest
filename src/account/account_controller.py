from fastapi import HTTPException
from typing import List
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config


from .account_service import AccountService
from .account_model import LoginCrediential, Account, AccountCreate, Token as TokenModel


@Controller("account", tag="account")
class AccountController:

    def __init__(self, account: AccountService):
        self.account = account

    @Get("/", response_model=List[Account])
    async def get_accounts(self, session: AsyncSession = Depends(config.get_db)):
        accounts = await self.account.get_accounts(session)
        return accounts

    @Post("/")
    async def register(self, account: AccountCreate, session: AsyncSession = Depends(config.get_db)):
        account_exist = await self.account.check_account_exist(account, session)
        if account_exist:
            raise HTTPException(status_code=409, detail="Account already exists")
        new_account = await self.account.add_account(account, session)
        return new_account
    
    @Post("/token", response_model=TokenModel)
    async def login(self, account: LoginCrediential, session: AsyncSession = Depends(config.get_db)):
        account_exist = await self.account.check_account_exist(account, session)
        if not account_exist:
            raise HTTPException(status_code=401, detail="Account does not exist")
        print(account_exist.password)
        if not self.account.verify_password(account.password, account_exist.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = self.account.create_access_token({"sub": account.username})
        refresh_token = await self.account.generate_refresh_token(account_exist.username, session)
        print(refresh_token,'The refresh token')
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