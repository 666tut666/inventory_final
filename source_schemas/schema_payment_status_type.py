from pydantic import BaseModel, Field, PositiveInt


class PaymentStatusTypeBase(BaseModel):
    name: str = Field(
        title="The NAME of the payment status type",
        description="Note: must be a string with a length of less than 50 characters",
        example="success",
        max_length=50,
    )


class PaymentStatusTypeCreate(PaymentStatusTypeBase):
    pass


class PaymentStatusTypeUpdate(PaymentStatusTypeBase):
    id: PositiveInt = Field(
        title="The ID of the payment status type",
        description="Note: must be a positive integer",
        example=1,
    )


class PaymentStatusTypeResponse(PaymentStatusTypeBase):
    id: PositiveInt = Field(
        title="The ID of the payment status type",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
