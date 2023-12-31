from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator


class UserBaseSchema(BaseModel):
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    name: str
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LoginUserSchema(UserBaseSchema):
    password: constr(min_length=8)


class UserPatchSchema(BaseModel):
    role: str | None = None
    is_active: bool | None = None

    @field_validator("role")
    def check_role(cls, role: str) -> str:
        if role not in ("admin", "user"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="wrong role",
            )
        return role


class UserAdminResponseSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    is_active: bool
    name: str
