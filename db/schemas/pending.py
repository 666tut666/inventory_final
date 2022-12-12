from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class Pending(BaseModel):
    title: str
    item_type: str
    category: str
    quantity: int
    creation_date: date
    id: Optional[int]
    email: EmailStr
    user_id: int
    admin_id: int

    class Config:
        orm_mode=True