from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from src.config import ALGORITHM
from src.config import SECRET_KEY
from src.dependency import get_db
from src.models.user import TokenData
from src.orm.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.user_name == username).first()


async def update_user_login_time(
    db: Session, user: User, time: datetime,
):
    user.last_login = time
    db.commit()
    return


async def authenticate_user(
    db: Session, username: str, password: str,
) -> Union[bool, User]:
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    await update_user_login_time(db, user, datetime.utcnow())
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # assertation needed to fix mypy
    assert isinstance(token_data.username, str)
    user = await get_user_by_username(db, username=token_data.username)
    assert user is not None
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def current_user_is_superuser(
    current_user: User = Depends(get_current_user),
) -> bool:
    if current_user.is_superuser is False:
        raise HTTPException(
            status_code=403, detail=f"User {current_user.user_name} is not SuperUser",
        )
    return True
