from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    id: int

    class Config:
        orm_mode = True
