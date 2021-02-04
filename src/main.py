import uvicorn

from src.crud import get_newspapers
from src.models.newspaper import NewsPaper
from src.orm.database import SessionLocal, engine, Base
from typing import List

from fastapi import Depends, FastAPI
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


@app.get("/newspapers/", response_model=List[NewsPaper])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    newspapers = get_newspapers(db, skip=skip, limit=limit)
    return newspapers


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
