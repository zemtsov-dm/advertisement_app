from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination import Page
from ..dependences import get_current_admin_user, get_current_user

from ..crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..schemas import UserAdminResponseSchema, UserResponseSchema, UserPatchSchema
from app.database import get_session

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", status_code=status.HTTP_200_OK)
async def self_user(user: User = Depends(get_current_user)) -> UserResponseSchema:
    return user


@router.get("", status_code=status.HTTP_200_OK)
async def get_users(
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> Page[UserResponseSchema]:
    return await UserCRUD.get_items(session)


@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def change_user(
    id: int,
    user_data: UserPatchSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_admin_user),
) -> UserAdminResponseSchema:
    target_user: User = UserCRUD.get_item_by_id(db=session,model_id=id)
    if target_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if user_data.role is not None:
        target_user.role = user_data.role
    if user_data.is_active is not None:
        target_user.is_active = user_data.is_active
    await session.commit()
    return target_user
