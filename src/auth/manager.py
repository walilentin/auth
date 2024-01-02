from typing import List, Callable

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.auth import utils
from src.core.database import get_async_session
from src.users.models import User
from jwt import InvalidTokenError

from src.users.schemas import UserSchemas

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


async def validate_auth_user(
        username: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_async_session),
):
    statement = select(User).filter(User.username == username)
    result = await session.execute(statement)
    user = result.scalar()

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if not user or not utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


async def create_access_token(
        # token_credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme),
):
    # token = token_credentials.credentials
    try:
        payload = utils.decode_jwt(token=token)

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
        )
    response = JSONResponse(content={"message": "Token created"})
    response.set_cookie(key="access_token", value=payload)
    return payload


async def get_current_user(token: str = Depends(create_access_token),
                           db: AsyncSession = Depends(get_async_session)):
    username: str = token.get("username")
    statement = select(User).filter(User.username == username)
    result = await db.execute(statement)
    user = result.scalar()

    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (user not found)",
        )


def has_role(allowed_roles: List[str] = Depends()) -> Callable[[UserSchemas], UserSchemas]:
    def check_role(user: UserSchemas = Depends(get_current_user)):
        if not any(role in user.roles for role in allowed_roles):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user

    return check_role


def current(user: UserSchemas = Depends(has_role(["user"]))):
    return user


def current_admin(user: UserSchemas = Depends(has_role(["admin"]))):
    return user
