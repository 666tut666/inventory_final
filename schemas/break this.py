from pydantic import EmailStr, BaseModel
from datetime import date
from typing import Optional


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    #user_id: Optional[int]
    admin_id: Optional[int]
    #admin_type_id: int

    class Config:
        orm_mode=True
        schema_extra = {
            'example': {
                "email":"your@email.com",
                "password":"yourPassword"
            }
        }


class ShowAdmin(BaseModel):
    email: EmailStr
    id: int

    class Config:
        orm_mode=True
            ##orm object relationship mapper
            ##object lai dictionary banayo


class ItemCreate(BaseModel):
    title: str
    type: str
    category: str
    quantity: int

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


class RequestStatus(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }


class ShowItem(BaseModel):
    title: str
    type: str
    category: str
    quantity: int
    date_posted: date

    class Config:
        orm_mode=True


class StaffCreate(BaseModel):
    email: EmailStr
    password: str
    staff_id: Optional[int]


class ShowStaff(BaseModel):
    email: EmailStr

    class Config:
        orm_mode=True
            ##orm object relationship mapper
            ##object lai dictionary banayo


class User(BaseModel):
    email: EmailStr
    password: str
    user_id: int
    admin_type_id: int
    staff_id: int
    id: int

