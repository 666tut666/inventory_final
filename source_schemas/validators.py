import re

from pydantic import BaseModel, validator

from app.utils.exceptions.common_exceptions import HTTPBadRequestException


class PasswordValidator(BaseModel):
    @validator("password", check_fields=False)
    def password_validator(cls, password: str) -> str:
        if not re.match(
            r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+|\\])[\s\S]{8,100}$", password
        ):
            raise HTTPBadRequestException(
                detail="Password must contain at least 1 uppercase letter, "
                "1 number and 1 special symbol (e.g. !@#$%^&*()-_=+|\\)"
            )
        return password


class PhoneNumberValidator(BaseModel):
    @validator("phone", check_fields=False)
    def phone_validator(cls, phone: str) -> str:
        if not re.match(r"^\+\d{12}$", phone):
            raise HTTPBadRequestException(
                detail="Phone number must be in the format: +[country code][phone number]"
            )
        return phone
