from pydantic import EmailStr, BaseModel

from typing import Optional



class RequestStatus(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }



class User(BaseModel):
    email: EmailStr
    password: str
    user_id: int
    id: int

