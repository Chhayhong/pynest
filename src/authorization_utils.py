from nest.core import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os

from src.account.account_entity import Account
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
from src.config import config
Not_Authorized_Message = "Not enough permissions"
async def get_current_account(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),session: AsyncSession = Depends(config.get_db)):
    if credentials.scheme == "Bearer":
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            account_id = int(payload.get('account_id'))
            account_username = payload.get('sub')
            query = await session.execute(select(Account).filter(Account.username == account_username))
            account = query.scalars().first()
            if account is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            if account.is_active == False:
                raise HTTPException(status_code=401, detail="Account is not active")
            return account_id
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
