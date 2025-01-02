
from fastapi import Depends, HTTPException
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

Not_Authorized_Message = "Not enough permissions"
def get_current_account(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if credentials.scheme == "Bearer":
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            account_id = payload.get('account_id')
            account_id = int(account_id)
            return account_id
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

