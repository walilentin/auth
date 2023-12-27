from fastapi import Depends
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


def get_auth_service(db_session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db_session)
