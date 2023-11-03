import logging

from fastapi import APIRouter, Depends, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.users.filters import UserFilter
from api.users.utils.users import change_status_user, set_admin

from ..crud import UserCRUD
from ..dependences import get_current_active_user, get_current_admin_user
from ..models import User
from ..schemas import (UserAdminResponseSchema, UserPatchSchema,
                       UserResponseSchema)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", status_code=status.HTTP_200_OK)
async def self_user(user: User = Depends(get_current_active_user)) -> UserResponseSchema:
    """Получение информации пользователя о себе"""
    logger.info("self_user")
    return user


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    user: User = Depends(get_current_admin_user),
    user_filter: UserFilter = FilterDepends(UserFilter),
    session: AsyncSession = Depends(get_session),
) -> Page[UserAdminResponseSchema]:
    """Получение информации о всех пользователях"""
    logger.info("Get all users")
    return await UserCRUD.get_items(db=session, user_filter=user_filter)


@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def change_user(
    id: int,
    user_data: UserPatchSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_admin_user),
) -> UserAdminResponseSchema:
    """Получение информации о конкретном пользователе"""
    logger.info("Change user")
    target_user: User = await UserCRUD.get_item_by_id(db=session,model_id=id)
    if user_data.role is not None:
        set_admin(target_user, user_data.role)
    if user_data.is_active is not None:
        change_status_user(target_user,user_data.is_active)
    await session.commit()
    return target_user
