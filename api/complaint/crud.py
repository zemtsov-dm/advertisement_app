from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_crud import BaseCRUD
from api.complaint.models import Complaint
from api.users.filters import UserFilter


class ComplaintCRUD(BaseCRUD):
    model = Complaint

    @classmethod
    async def get_items(
        cls,
        advert_id: int,
        db: AsyncSession,
        user_filter: UserFilter,
    ):
        stmt = select(cls.model).where(cls.model.advert_id == advert_id)
        stmt = user_filter.filter(stmt)
        stmt = user_filter.sort(stmt)
        result = await paginate(db, stmt)
        return result
