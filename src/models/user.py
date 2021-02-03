from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: str
    user_name: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
