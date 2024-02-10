import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, AuthProvider, get_settings
from app.config import Settings
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()



@router.post(
    path="/register",
    description="Register user",
    response_model=dto.User
)
async def register_user(
        user: schems.RegisterUser,
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.User:
    current_user = await dao.user.get_user(email=user.email)
    if current_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
    auth = AuthProvider(settings=settings)
    user = await dao.user.add_user(
        full_name=user.full_name,
        email=user.email,
        password=auth.get_password_hash(password=user.password),
        limit=100,
        api_key=uuid.uuid4().hex
    )
    return user
