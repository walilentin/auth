from fastapi import APIRouter, Depends

from src.auth.manager import current_admin, get_current_user, has_role
from src.auth.service import AuthService, get_auth_service
from src.users.schemas import UserSchemas, UserUpgrade

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me/", response_model=UserSchemas)
def auth_user_check_self_info(
        user: UserSchemas = Depends(get_current_user),
):
    return user


@router.get("/hello_admin")
async def auth_user_check(
        user: UserSchemas = Depends(current_admin),
):
    return {"Hello!": f"{user.username}, you are admin."}


@router.post("/users/{user_id}/update-roles", dependencies=[Depends(has_role("admin"))])
async def update_user_roles(
        user_id: int,
        user_data: UserUpgrade,
        service: AuthService = Depends(get_auth_service)
):
    return await service.update_roles(user_id, user_data.roles)
