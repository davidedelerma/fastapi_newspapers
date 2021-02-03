from src.models.user import UserCreate
from sqlalchemy.orm.session import Session

from src.orm import newspaper as ns
from src.orm import user as us


def get_newspaper(db: Session, newspaper_id: int):
    return db.query(ns.NewsPaper).filter(ns.NewsPaper.id == newspaper_id).first()


def get_newspapers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ns.NewsPaper).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(us.User).filter(us.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(us.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = us.User(
        email=user.email,
        user_name=user.user_name,
        first_name=user.first_name,
        last_name=user.last_name,
        password=fake_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
