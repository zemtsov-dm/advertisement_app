from pydantic import BaseModel, EmailStr, constr, ConfigDict

# from app.adverts.schemas import AdvertBase


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
    id: int
    role: str | None = None
    is_active: bool | None = None


class UserAdminResponseSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    is_active: bool
