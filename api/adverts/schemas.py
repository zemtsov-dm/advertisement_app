from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator


class AdvertBase(BaseModel):
    title: str
    description: str | None = None
    ad_type: str
    price: int

    @field_validator("ad_type")
    def check_type(cls, type: str) -> str:
        if type not in ("Покупка", "Продажа", "Оказание услуг"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="wrong type",
            )
        return type
class AdvertCreate(AdvertBase):
    pass


class AdvertResponse(AdvertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime

class AdvertChange(BaseModel):
    ad_type: str

    @field_validator("ad_type")
    def check_type(cls, type: str) -> str:
        if type not in ("Покупка", "Продажа", "Оказание услуг"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="wrong type",
            )
        return type