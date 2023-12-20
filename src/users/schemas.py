from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    password: str


class UserSchemas(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True

