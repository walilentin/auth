from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.auth import utils
from src.core.curl import BaseService
from src.core.database import get_async_session
from src.users.models import User


class AuthService(BaseService[User]):
    def __init__(self, db_session: Session):
        super(AuthService, self).__init__(User, db_session)

    async def create(self, data):
        async with self.db_session as session:
            hashed_password = utils.hash_password(data.password)
            new_user = self.table(
                username=data.username,
                email=data.email,
                password=hashed_password,
            )
            session.add(new_user)
            await session.commit()
        return new_user

    async def update_roles(self, user_id: int, roles: List[str]):
        async with self.db_session as session:
            try:
                user = await self.get_one(user_id)
                if user:
                    user.roles = roles
                    session.add(user)
                    await session.commit()
                    return user
                else:
                    print(f"User with ID {user_id} not found.")
                    raise HTTPException(status_code=404, detail="User not found")
            except Exception as e:
                print(f"Error updating roles: {e}")
                await session.rollback()
                raise HTTPException(status_code=500, detail="Internal Server Error")


def get_auth_service(db_session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db_session)
