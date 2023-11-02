from fastapi import APIRouter, Depends, status
from ..dependences import get_current_admin_user, get_current_user

from ..crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..schemas import UserAdminResponseSchema, UserResponseSchema, UserPatchSchema
from fastapi import HTTPException, status
from app.database import get_session

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", status_code=status.HTTP_200_OK)
async def self_user(user: User = Depends(get_current_user))-> UserResponseSchema:
    return user


@router.get("", status_code=status.HTTP_200_OK)
async def get_users(
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session),
) -> list[UserResponseSchema]:
    return await UserCRUD.get_items(session)


@router.patch("", status_code=status.HTTP_201_CREATED)
async def change_user(
    user_data: UserPatchSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> UserAdminResponseSchema:  
    user = await UserCRUD.get_item_by_id(db = session,model_id=user_data.id)
    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    await session.commit()
    return user
