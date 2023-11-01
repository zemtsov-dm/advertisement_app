from pydantic import BaseModel

from app.adverts.schemas import AdvertBase

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_admin: bool
    items: list[AdvertBase] = []

    class Config:
        orm_mode = True
