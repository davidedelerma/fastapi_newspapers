from sqlalchemy import Column, UniqueConstraint, Integer, String
from .database import Base


class NewsPaper(Base):
    __tablename__ = "newspapers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    year_of_fundation = Column(Integer)
    nationality = Column(String)
    director = Column(String)
    political_orientation = Column("orientation", String)
    __table_args__ = (
        UniqueConstraint("name", "nationality", name="_name_nationality_uc"),
    )
