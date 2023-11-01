from pydantic import BaseModel, EmailStr, constr

from app.adverts.schemas import AdvertBase


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=8)
    passwordConfirm: str
    role: str = "user"


class User(UserBase):
    id: int
    role: str
    adverts: list[AdvertBase] = []

    class Config:
        orm_mode = True


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
