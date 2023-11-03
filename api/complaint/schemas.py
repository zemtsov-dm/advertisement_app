import datetime

from pydantic import BaseModel, ConfigDict


class ComplaintBaseSchema(BaseModel):
    title: str
    description: str


class ComplaintCreateSchema(ComplaintBaseSchema):
    pass


class ComplaintResponseSchema(ComplaintBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    advert_id: int
    user_id: int
    created_at: datetime.datetime
