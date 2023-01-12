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





## Trying new method for pending, allowed, taken and returned

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    user_id:Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }
