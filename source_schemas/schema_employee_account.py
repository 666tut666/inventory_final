from datetime import date

from pydantic import BaseModel, Field, FutureDate, PositiveInt


class EmployeeAccountBase(BaseModel):
    name: str = Field(
        title="The NAME of the employee account",
        description="Note: must be a string with a length of less than 100 characters",
        example="PB",
        max_length=100,
    )
    number: str = Field(
        title="The NAME of the employee account",
        description="Note: must be a string with a length of less than 50 characters",
        example="1234567890",
        max_length=50,
    )
    is_default: bool = Field(
        title="The DEFAULT/NOT DEFAULT STATUS of the employee account",
        description="Note: must be 'True' or 'False'",
        example=True,
    )
    issuer: str = Field(
        title="The CARD ISSUER of the employee account",
        description="Note: must be a string with a length of less than 100 characters",
        example="PB",
        max_length=100,
    )
    deactivation_date: FutureDate = Field(
        title="The DATE of the employee account deactivation",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2023-01-01",
    )
    account_type_id: PositiveInt = Field(
        title="The ID of the account type",
        description="Note: must be a positive integer",
        example=1,
    )


class EmployeeAccountCreate(EmployeeAccountBase):
    employee_id: PositiveInt = Field(
        title="The ID of the employee",
        description="Note: must be a positive integer",
        example=1,
    )


class EmployeeAccountUpdate(EmployeeAccountBase):
    id: PositiveInt = Field(
        title="The ID of the employee account",
        description="Note: must be a positive integer",
        example=1,
    )
    is_active: bool = Field(
        title="The ACTIVE/NOT ACTIVE STATUS of the employee account",
        description="Note: must be 'True' or 'False'",
        example=True,
    )


class EmployeeAccountResponse(EmployeeAccountBase):
    id: PositiveInt = Field(
        title="The ID of the employee account",
        description="Note: must be a positive integer",
        example=1,
    )
    is_active: bool = Field(
        title="The ACTIVE/NOT ACTIVE STATUS of the employee account",
        description="Note: must be 'True' or 'False'",
        example=True,
    )
    creation_date: date = Field(
        title="The CREATION DATE of the payment method",
        description="Note: must be a date with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    employee_id: PositiveInt = Field(
        title="The ID of the employee",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
