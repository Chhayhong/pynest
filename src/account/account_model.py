from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing_extensions import Self
import re

class AccountCreate(BaseModel):
    username: str = Field(min_length=6, max_length=32)
    password: str = Field(min_length=6, max_length=64)
    password_confirmation: str = Field(min_length=6, max_length=64)
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_confirmation:
            raise ValueError('Passwords do not match')
        return self
    
    @model_validator(mode='after')
    def check_username_validation(self) -> Self:
        if self.username:
            if len(self.username) < 6:
                raise ValueError('Username must be at least 6 characters long')
            if len(self.username) > 64:
                raise ValueError('Username must be at most 32 characters long')
            if not re.match("^[a-zA-Z0-9_]*$", self.username):
                raise ValueError('Username can only contain alphanumeric characters and underscores')
            if re.search(r"([_]{2,})", self.username):
                raise ValueError('Username cannot contain consecutive underscores')
            if re.search(r"([0-9]{3,})", self.username):
                raise ValueError('Username cannot contain consecutive numbers')
        else:
            raise ValueError('Username is required')
        return self
    
class Account(BaseModel):
    account_id: int
    username: str 
    email: EmailStr = Field(exclude=True)
    role: str = "user"
    class Config:
        orm_mode = True

class AccountsResponse(BaseModel):
    account_id: int
    username: str 
    email: Optional[EmailStr] 
    role: str = "user"
    is_active: bool
    class Config:
        orm_mode = True

class LoginCrediential(BaseModel):
    username: str = Field(min_length=6, max_length=32)
    password: str = Field(min_length=6, max_length=64)

class LogoutSuccess(BaseModel):
    detail: str = "Logged out successfully"

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class AccountUpdateStatus(BaseModel):
    is_active: bool