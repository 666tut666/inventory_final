from pydantic import BaseModel, Field, PositiveInt


class RoleBase(BaseModel):
    name: str = Field(
        title="The NAME of the role",
        description="Note: must be a string with a length of less than 50 characters",
        example="admin",
        max_length=50,
    )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    id: PositiveInt = Field(
        title="The ID of the role",
        description="Note: must be a positive integer",
        example=1,
    )


class RoleResponse(RoleBase):
    id: PositiveInt = Field(
        title="The ID of the role",
        description="Note: must be a positive integer",
        example=1,
    )

    class Config:
        orm_mode = True
