from pydantic import EmailStr, BaseModel

from typing import Optional

class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    owner_id: Optional[int]
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

