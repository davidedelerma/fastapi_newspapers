from datetime import timedelta

import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.auth import authenticate_user, create_access_token, get_current_active_user
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.crud import get_newspapers
from src.models.newspaper import NewsPaper
from src.models.user import User, Token
from src.orm.database import SessionLocal, engine, Base
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = user.user_name
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/newspapers/", response_model=List[NewsPaper])
def read_newspapers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    newspapers = get_newspapers(db, skip=skip, limit=limit)
    return newspapers


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
