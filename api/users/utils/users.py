
from fastapi import HTTPException, status

from api.users.models import User


def set_admin(target_user: User, role: str) -> User:
    if target_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    target_user.role = role

def change_status_user(target_user: User, status: bool) -> User:
    target_user.is_active = status