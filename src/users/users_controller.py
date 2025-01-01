from http.client import HTTPException
from typing import List
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config


from .users_service import UsersService
from .users_model import LoginCrediential, User, UserCreate, Token as TokenModel


@Controller("users", tag="users")
class UsersController:

    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @Get("/", response_model=List[User])
    async def get_users(self, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.get_users(session)

    @Post("/")
    async def register(self, user: UserCreate, session: AsyncSession = Depends(config.get_db)):
        user_exist = await self.users_service.check_user_exist(user,session)
        if user_exist:
            return {"detail": "User already exists."}
        return await self.users_service.add_user(user, session)
    
    @Post("/token", response_model=TokenModel)
    async def login(self, user: LoginCrediential, session: AsyncSession = Depends(config.get_db)):
        user_exist = await self.users_service.check_user_exist(user, session)
        if not user_exist:
            return {"detail": "User does not exist."}
        print(user_exist.password)
        if not self.users_service.verify_password(user.password, user_exist.password):
            return {"detail": "Incorrect password."}
        access_token = self.users_service.create_access_token(
            {"sub": user.username}
        )
        print(user_exist.id,'Show id......')
        refresh_token =await self.users_service.generate_refresh_token(user_exist.username, session)
        print(refresh_token,'The refresh token')
        return {"access_token": access_token, "token_type": "bearer","refresh_token":refresh_token}
    
    @Get("/me", response_model=User)
    async def get_current_user(self, token: str, session: AsyncSession = Depends(config.get_db)):
        username = self.users_service.verify_token(token)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
        
        user = await self.users_service.check_username_exist(username, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    @Post("/logout")
    async def logout(self, token: str, session: AsyncSession = Depends(config.get_db)):
        username = self.users_service.verify_token(token)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
        
        user = await self.users_service.check_username_exist(username, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.refresh_token = None
        await session.commit()
        
        return {"detail": "Logged out successfully"}

        