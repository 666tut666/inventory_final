from pydantic import BaseModel, Field, PositiveInt


class StatusTypeBase(BaseModel):
    name: str = Field(
        title="The NAME of the status type",
        description="Note: must be a string with a length of less than 50 characters",
        example="not active",
        max_length=50,
    )


class StatusTypeCreate(StatusTypeBase):
    pass


class StatusTypeUpdate(StatusTypeBase):
    id: PositiveInt = Field(
        title="The ID of the status type",
        description="Note: must be a positive integer",
        example=1,
    )


class StatusTypeResponse(StatusTypeBase):
    id: PositiveInt = Field(
        title="The ID of the status type",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
