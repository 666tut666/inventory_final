from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field


class SessionBase(BaseModel):
    token: str
    creation_date: datetime
    status: str


class SessionCreate(SessionBase):
    user_id: Optional[PositiveInt] = None


class SessionUpdate(SessionBase):
    id: PositiveInt
    token: Optional[str] = None
    creation_date: Optional[datetime] = None
    status: Optional[str] = None
    user_id: Optional[PositiveInt] = None
