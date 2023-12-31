from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_session
from api.users.models import User
from config import settings

from .crud import UserCRUD


def get_token(request: Request):
    token = request.cookies.get("advertisement_app_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_active_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(get_token),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM,
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UserCRUD.get_item_by_id(db=session, model_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


async def get_current_admin_user(user: User = Depends(get_current_active_user)):
    if not user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
