from pydantic import BaseModel, EmailStr

class AccountCreate(BaseModel):
    username: str
    password: str
    
class Account(BaseModel):
    account_id: int
    username: str
    email: EmailStr
    role: str = "user"
    class Config:
        orm_mode = True

class LoginCrediential(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str