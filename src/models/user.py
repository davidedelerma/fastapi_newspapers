import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator


class UserBase(BaseModel):
    email: EmailStr
    user_name: str
    first_name: str
    last_name: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_validation(cls, v):
        """
        password must contain minimum six characters, at least one letter,
        one number and one special character
        """
        if not re.fullmatch(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$', v,
        ):
            raise ValueError(
                'passwords must contain minimum six characters, '
                'at least one letter, one number and one special character ',
            )
        return v


class User(UserBase):
    id: int
    last_login: Optional[datetime]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
