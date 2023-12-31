import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.users.utils.auth import (authenticate_user, create_access_token,
                                  get_password_hash)

from ..crud import UserCRUD
from ..models import User
from ..schemas import LoginUserSchema, UserCreateSchema

logger = logging.getLogger(__name__) 

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register")
async def register_user(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    """Регистрация пользователя"""
    logger.info("Register user")
    existing_user = await UserCRUD.get_filtered_item(session, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist",
        )
    hashed_password = get_password_hash(user_data.password)
    await UserCRUD.add_item(
        session,
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name,
    )


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(
    response: Response,
    user_data: LoginUserSchema,
    session: AsyncSession = Depends(get_session),
):
    """Получение токена JWT"""
    logger.info("Login user")
    user: User = await authenticate_user(
        session=session,
        email=user_data.email,
        password=user_data.password,
    )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        "advertisement_app_token",
        access_token,
        httponly=True,
    )
    return access_token


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    """Выход пользователя из системы"""
    logger.info("Logout user")
    response.delete_cookie("advertisement_app_token")
    return "success logout"
