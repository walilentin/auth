from typing import Annotated, List

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, validator

class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    password: str


class UserSchemas(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: EmailStr | None = None
    active: bool = True
    roles: List[str] = []

    @validator("roles", pre=True, always=True)
    def set_roles_default(cls, v):
        return v if v is not None else []

class Token_info(BaseModel):
    access_token: str
    token_type: str


class UserUpgrade(BaseModel):
    roles: List[str]

    @validator("roles")
    def validate_roles(cls, v):
        if not v:
            raise ValueError("Roles list must not be empty")
        return v


