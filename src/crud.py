from src.models import newspaper as ns
from sqlalchemy.orm.session import Session


def get_newspaper(db: Session, newspaper_id: int):
    return db.query(ns.NewsPaper).filter(ns.NewsPaper.id == newspaper_id).first()


def get_newspapers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ns.NewsPaper).offset(skip).limit(limit).all()
