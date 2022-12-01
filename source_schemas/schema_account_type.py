from pydantic import BaseModel, Field, PositiveInt


class AccountTypeBase(BaseModel):
    name: str = Field(
        title="The NAME of the account type",
        description="Note: must be a string with a length of less than 50 characters",
        example="card",
        max_length=50,
    )


class AccountTypeCreate(AccountTypeBase):
    pass


class AccountTypeUpdate(AccountTypeBase):
    id: PositiveInt = Field(
        title="The ID of the account type",
        description="Note: must be a positive integer",
        example=1,
    )


class AccountTypeResponse(AccountTypeBase):
    id: PositiveInt = Field(
        title="The ID of the account type",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
