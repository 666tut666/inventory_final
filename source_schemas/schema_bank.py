from datetime import date

from pydantic import BaseModel, Field, PositiveInt, FutureDate


class BankBase(BaseModel):
    name: str = Field(
        title="The NAME of the bank",
        description="Note: must be a string with a length of less than 50 characters",
        example="OneDollar",
        max_length=50,
    )
    mfo: str = Field(
        title="The MFO of the bank",
        description="Note: must be a string with a length of less than 50 characters",
        example="123456",
        max_length=50,
    )
    deactivation_date: FutureDate = Field(
        title="The DATE of the payment method deactivation",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2023-01-01",
    )


class BankCreate(BankBase):
    pass


class BankUpdate(BankBase):
    id: PositiveInt = Field(
        title="The ID of the bank",
        description="Note: must be a positive integer",
        example=1,
    )
    is_active: bool = Field(
        title="The ACTIVE/NOT ACTIVE STATUS of the bank",
        description="Note: must be 'True' or 'False'",
        example=True,
    )


class BankResponse(BankBase):
    id: PositiveInt = Field(
        title="The ID of the bank",
        description="Note: must be a positive integer",
        example=1,
    )
    is_active: bool = Field(
        title="The STATUS of the bank",
        description="Note: must be 'True' or 'False'",
        example=True,
    )
    creation_date: date = Field(
        title="The CREATION DATE of the bank",
        description="Note: must be a date with format: yyyy-mm-dd",
        example="2022-01-01",
    )

    class Config:
        orm_mode = True
