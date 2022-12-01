from pydantic import BaseModel, Field, PositiveInt


class EmployerTypeBase(BaseModel):
    name: str = Field(
        title="The NAME of the employer type",
        description="Note: must be a string with a length of less than 50 characters",
        example="AT",
        max_length=50,
    )


class EmployerTypeCreate(EmployerTypeBase):
    pass


class EmployerTypeUpdate(EmployerTypeBase):
    id: PositiveInt = Field(
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example=1,
    )


class EmployerTypeResponse(EmployerTypeBase):
    id: PositiveInt = Field(
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
