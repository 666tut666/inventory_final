from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PositiveInt

from app.schemas.validators import PasswordValidator, PhoneNumberValidator


class UserBase(BaseModel):
    email: EmailStr = Field(
        title="The EMAIL of the user",
        description="Note: must be a valid e-mail address with format: [account name]@[domain name].[domain extension]",
        example="example@mail.com",
    )
    phone: Optional[str] = Field(
        title="The PHONE NUMBER of the user",
        description="Note: must be a valid phone number with format: +[country code][phone number]",
        example="+380123456789",
        min_length=13,
        max_length=50,
    )


class UserCreate(UserBase, PasswordValidator, PhoneNumberValidator):
    password: str = Field(
        title="The PASSWORD of the user account",
        description="Note: must be a string with a length of more than 8 and less than 100 characters, "
        "containing at least 1 uppercase character, 1 number and 1 special symbol (e.g. !@#$%^&*()-_=+|\\)",
        example="Password1!",
        min_length=8,
        max_length=100,
    )


class UserUpdate(UserBase, PasswordValidator, PhoneNumberValidator):
    role_id: PositiveInt = Field(
        title="The ID of the role of the user",
        description="Note: must be a positive integer",
        example=1,
    )
    status_type_id: PositiveInt = Field(
        title="The ID of the status type of the user",
        description="Note: must be a positive integer",
        example=1,
    )


class UserResponse(UserBase):
    role_id: PositiveInt = Field(
        title="The ID of the role of the user",
        description="Note: must be a positive integer",
        example=1,
    )
    status_type_id: PositiveInt = Field(
        title="The ID of the status type of the user",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
