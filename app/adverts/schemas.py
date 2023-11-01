from pydantic import BaseModel


class AdvertBase(BaseModel):
    title: str
    description: str | None = None
    type: str
    price: int


class ItemCreate(AdvertBase):
    pass


class Item(AdvertBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
