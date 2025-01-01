from .users_model import LoginCrediential, UserCreate
from .users_entity import Users as UsersEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_REFRESH_TOKEN_MINUTES = int(os.getenv("ACCESS_REFRESH_TOKEN_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@Injectable
class UsersService:

    @async_db_request_handler
    async def add_user(self, user: UserCreate, session: AsyncSession):
        new_user = UsersEntity(
            **user.model_dump()
        )
        new_user.password = self.get_password_hash(user.password)
        session.add(new_user)
        await session.commit()
        return new_user.id

    @async_db_request_handler
    async def get_users(self, session: AsyncSession):
        query = select(UsersEntity)
        result = await session.execute(query)
        return result.scalars().all()
    @async_db_request_handler
    async def authenticate_user(self, user: LoginCrediential, session: AsyncSession):
        query = select(UsersEntity).where(
        UsersEntity.username == user.username,
        UsersEntity.password == self.get_password_hash(user.password)
        )
        result = await session.execute(query)
        return result.scalars().first()
    
    @async_db_request_handler
    async def check_user_exist(self,user:UserCreate, session: AsyncSession):
        query = select(UsersEntity).where(
        UsersEntity.username == user.username)
        result = await session.execute(query)
        return result.scalars().one_or_none()
    
    @async_db_request_handler
    async def check_username_exist(self,username:str, session: AsyncSession):
        query = select(UsersEntity).where(
        UsersEntity.username == username)
        result = await session.execute(query)
        return result.scalars().first()

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except jwt.PyJWTError:
            return None
        
    @async_db_request_handler
    async def generate_refresh_token(self, username: str, session: AsyncSession):
        print(username,'username')
        query = select(UsersEntity).where(
        UsersEntity.username == username)
        result = await session.execute(query)
        user = result.scalars().one_or_none()    
        if user:
            refresh_token = self.create_refresh_token({"sub": user.username})
            user.refresh_token = refresh_token
            await session.commit()
            return refresh_token
        else:
            return None

    @async_db_request_handler
    async def refresh_access_token(self, refresh_token: str, session: AsyncSession):
        query = select(UsersEntity).where(UsersEntity.refresh_token == refresh_token)
        user = await session.execute(query).scalar()

        if user:
            access_token = self.create_access_token({"sub": user.username})
            return access_token
        else:
            return None

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=ACCESS_REFRESH_TOKEN_MINUTES) 
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(encoded_jwt,'Weee')
        return encoded_jwt