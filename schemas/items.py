from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    title: str
    type: str
    category: str
    quantity: int
    id: Optional[int]
    creation_date: Optional[datetime]

    class Config:
        orm_mode=True
        #schema_extra = {
        #    'example': {
        #        "Title":"String",
        #        "Type":"String",
        #        "Category":"String",
        #        "quantity":"Integer"
        #    }
        #}


class ShowItem(BaseModel):
    title: str
    type: str
    category: str
    quantity: int

    class Config:
        orm_mode=True
