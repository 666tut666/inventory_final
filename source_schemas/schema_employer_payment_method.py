from datetime import date

from pydantic import BaseModel, Field, FutureDate, PositiveInt


class EmployerPaymentMethodBase(BaseModel):
    iban: str = Field(
        title="The IBAN of the payment method",
        description="Note: must be a string with a length of less than 50 characters",
        example="UA1234567890",
        max_length=50,
    )
    deactivation_date: FutureDate = Field(
        title="The DATE of the payment method deactivation",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2023-01-01",
    )
    bank_id: PositiveInt = Field(
        title="The ID of the bank",
        description="Note: must be a positive integer",
        example=1,
    )


class EmployerPaymentMethodCreate(EmployerPaymentMethodBase):
    employer_id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1,
    )


class EmployerPaymentMethodUpdate(EmployerPaymentMethodBase):
    id: PositiveInt = Field(
        title="The ID of the payment method",
        description="Note: must be a positive integer",
        example=1,
    )
    is_active: bool = Field(
        title="The ACTIVE/NOT ACTIVE STATUS of the payment method",
        description="Note: must be 'True' or 'False'",
        example=True,
    )


class EmployerPaymentMethodResponse(EmployerPaymentMethodBase):
    id: PositiveInt = Field(
        title="The ID of the payment method",
        description="Note: must be a positive integer",
        example=1,
    )
    is_active: bool = Field(
        title="The ACTIVE/NOT ACTIVE STATUS of the payment method",
        description="Note: must be 'True' or 'False'",
        example=True,
    )
    creation_date: date = Field(
        title="The CREATION DATE of the payment method",
        description="Note: must be a date with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    employer_id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
