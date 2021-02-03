from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.sql.sqltypes import DateTime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime)
