from enum import Enum
from pydantic import BaseModel, Field


class Orientation(str, Enum):
    left = "left"
    right = "right"


class NewsPaperBase(BaseModel):
    name: str
    year_of_fundation: int
    nationality: str
    director: str
    political_orientation: Orientation = Field(None, alias="Orientation")


class NewsPaperCreate(NewsPaperBase):
    pass


class NewsPaper(NewsPaperBase):
    id: int

    class Config:
        orm_mode = True
