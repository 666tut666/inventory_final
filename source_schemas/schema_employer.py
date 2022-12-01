from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, FutureDate, PositiveInt

from app.schemas.schema_user import UserBase, UserCreate, UserResponse, UserUpdate


class EmployerBase(BaseModel):
    user: UserBase
    name: str = Field(
        title="The NAME of the employer",
        description="Note: must be a string with a length of less than 100 characters",
        example="Example Company",
        max_length=100,
    )
    address: str = Field(
        title="The ADDRESS of the employer",
        description="Note: must be a string with a length of less than 100 characters",
        example="1 STREET st LOCALITY",
        max_length=100,
    )
    edrpou: str = Field(
        title="The EDRPOU of the employer",
        description="Note: must be a string with a length of less than 50 characters",
        example="12345678",
        max_length=50,
    )
    expire_contract_date: Optional[FutureDate] = Field(
        title="The DATE of the contract expiration",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2023-01-01",
    )
    salary_date: Optional[date] = Field(
        title="The DATE of the salary",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    prepayment_date: Optional[date] = Field(
        title="The DATE of the prepayment",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    employer_type_id: PositiveInt = Field(
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example=1,
    )


class EmployerCreate(EmployerBase):
    user: UserCreate


class EmployerUpdate(EmployerBase):
    id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1,
    )
    user: UserUpdate


class EmployerResponse(EmployerBase):
    id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1,
    )
    user: UserResponse

    class Config:
        orm_mode = True
