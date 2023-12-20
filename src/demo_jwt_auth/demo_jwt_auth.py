from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils
from src.core.database import get_async_session
from src.users.models import User
from src.users.schemas import UserSchemas
from jwt import InvalidTokenError

router = APIRouter(prefix='/jwt', tags=['JWT'])

http_bearer = HTTPBearer()


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_async_session)
):
    # Use the asynchronous session to query the user
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

class Token_info(BaseModel):
    access_token: str
    token_type: str



@router.post('/login', response_model=Token_info)
async def auth_user_jwt(
    user: User = Depends(validate_auth_user),
):
    token = utils.encode_jwt(
        id=user.id,
        username=user.username,
        email=user.email,
    )
    return Token_info(
        access_token=token,
        token_type='Bearer'
    )


async def get_current_token_payload(
        token_credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchemas:
    token = token_credentials.credentials
    try:
        payload = utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
        )
    return payload


async def get_current_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> UserSchemas:
    username: str | None = payload.get("username")

    # Use the asynchronous session to query the user
    statement = select(User).filter(User.username == username)
    result = await session.execute(statement)
    user = result.scalar()

    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (user not found)",
        )


async def get_current_active_user(
        user: UserSchemas = Depends(get_current_user)
):
    if user.active:
        return user
    raise HTTPException(status.HTTP_403_FORBIDDEN,
                        detail='user unactive')


@router.get("/me")
async def auth_user_check(
        user: UserSchemas = Depends(get_current_active_user)
):
    return {
        user.id,
        user.username,
        user.email,
        user.active,
    }
