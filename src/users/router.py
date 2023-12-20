from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import utils
from src.core.database import get_async_session
from src.users.models import User
from src.users.schemas import CreateUser, UserSchemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post('/create', response_model=UserSchemas)
async def create_user(
    user_data: CreateUser,
    session: AsyncSession = Depends(get_async_session)
):
    existing_user = await session.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already exists'
        )

    try:
        hashed_password = utils.hash_password(user_data.password)

        new_user = UserSchemas(
            username=user_data.username,
            password=hashed_password,
            email=user_data.email
        )

        user_model = User(
            username=new_user.username,
            password=hashed_password,
            email=new_user.email,
            active=True
        )


        session.add(user_model)
        await session.commit()
        return new_user

    except Exception as e:
        await session.rollback()
        raise e