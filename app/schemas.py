import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from pydantic_settings import BaseSettings


class createUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class userLogin(BaseModel):
    email: EmailStr
    password: str


class userResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class postBase(BaseModel):
    title: str
    content: str
    published: bool = True


class postCreate(postBase):
    pass


class postResponse(postBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: userResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
