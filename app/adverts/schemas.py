from pydantic import BaseModel, ConfigDict


class AdvertBase(BaseModel):
    title: str
    description: str | None = None
    type: str
    price: int


class ItemCreate(AdvertBase):
    pass


class Item(AdvertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int

    class Config:
        orm_mode = True
