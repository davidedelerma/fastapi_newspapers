from passlib.context import CryptContext

from src.auth import pwd_context
from src.models.user import UserCreate
from sqlalchemy.orm.session import Session

from src.orm import newspaper as ns
from src.orm import user as orm_user


def get_newspaper(db: Session, newspaper_id: int):
    return db.query(ns.NewsPaper).filter(ns.NewsPaper.id == newspaper_id).first()


def get_newspapers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ns.NewsPaper).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_pass = pwd_context.hash(user.password)
    db_user = orm_user.User(
        email=user.email,
        user_name=user.user_name,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_pass,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(orm_user.User).filter(orm_user.User.email == email).first()
