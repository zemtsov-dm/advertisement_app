from pydantic import BaseModel, EmailStr, constr, ConfigDict

# from app.adverts.schemas import AdvertBase


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    password: constr(min_length=8)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LoginUserSchema(UserBase):
    password: constr(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
