from pydantic import BaseModel
from typing import Optional
from datetime import date


class ItemCreate(BaseModel):
    title: str
    item_type: str
    category: str
    quantity: int
    #id: Optional[int]

    class Config:
        orm_mode=True

    #class Config:
        #orm_mode=True
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
    item_type: str
    category: str
    quantity: int
    creation_date: date

    class Config:
        orm_mode=True
