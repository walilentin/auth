from fastapi import APIRouter, Depends

from src.auth.manager import current_user
from src.users.schemas import UserSchemas

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me/", response_model=UserSchemas)
def auth_user_check_self_info(
    user: UserSchemas = Depends(current_user),
):
    return user

@router.get("/hello")
async def auth_user_check(
    user: UserSchemas = Depends(current_user),
):
    return {"Hello!": user.username}


