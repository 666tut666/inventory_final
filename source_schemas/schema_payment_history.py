from datetime import date

from pydantic import BaseModel, Field, PositiveInt


class PaymentHistoryBase(BaseModel):
    amount: PositiveInt = Field(
        title="The AMOUNT of the payment",
        description="Note: must be a positive integer",
        example=123456789,
    )


class PaymentHistoryCreate(PaymentHistoryBase):
    pass


class PaymentHistoryUpdate(PaymentHistoryBase):
    id: PositiveInt = Field(
        title="The ID of the payment history",
        description="Note: must be a positive integer",
        example=1,
    )
    payment_status_type_id: PositiveInt = Field(
        title="The ID of the payment status",
        description="Note: must be a positive integer",
        example=1,
    )


class PaymentHistoryResponse(PaymentHistoryBase):
    id: PositiveInt = Field(
        title="The ID of the payment history",
        description="Note: must be a positive integer",
        example=1,
    )
    creation_date: date = Field(
        title="The CREATION DATE of the payment history",
        description="Note: must be a date with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    employee_account_id: PositiveInt = Field(
        title="The ID of the employee account",
        description="Note: must be a positive integer",
        example=1,
    )
    employer_payment_method_id: PositiveInt = Field(
        title="The ID of the employer payment method",
        description="Note: must be a positive integer",
        example=1,
    )
    payment_status_type_id: PositiveInt = Field(
        title="The ID of the payment status",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
