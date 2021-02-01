from src.orm.database import SessionLocal, engine, Base
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud
from .models import newspaper as ns_model

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/newspapers/", response_model=List[ns_model.NewsPaper])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    newspapers = crud.get_newspapers(db, skip=skip, limit=limit)
    return newspapers
