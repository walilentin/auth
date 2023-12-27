import fastapi
from fastapi import Depends
from src.auth import utils
from src.auth.manager import validate_auth_user
from src.auth.service import AuthService, get_auth_service
from src.users.models import User
from src.users.schemas import CreateUser, UserSchemas, Token_info

router = fastapi.APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/login', response_model=Token_info)
async def auth_user_jwt(
        user: User = Depends(validate_auth_user),
):
    if user:
        token = utils.encode_jwt(
            username=user.username,
            email=user.email,
        )
        return Token_info(
            access_token=token,
            token_type="Bearer",
        )
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


@router.post('/create', response_model=UserSchemas)
async def create_user(
        user_data: CreateUser,
        service: AuthService = fastapi.Depends(get_auth_service),
):
    return await service.create(user_data)
