import logging

from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.filters import UserFilter

logger = logging.getLogger(__name__)


class BaseCRUD:
    model = None

    @classmethod
    async def get_item_by_id(
        cls,
        model_id: int,
        db: AsyncSession,
    ):
        model = await db.get(cls.model, model_id)
        logger.debug(model)
        if not model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return model

    @classmethod
    async def get_filtered_item(
        cls,
        db: AsyncSession,
        **filter_by,
    ):
        stmt = select(cls.model).filter_by(**filter_by)
        logger.debug(stmt)
        result: Result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_items(
        cls,
        db: AsyncSession,
        user_filter: UserFilter,
    ):
        stmt = select(cls.model)
        stmt = user_filter.filter(stmt)
        stmt = user_filter.sort(stmt)
        logger.debug(stmt)
        result = await paginate(db, stmt)
        return result

    @classmethod
    async def add_item(
        cls,
        db: AsyncSession,
        **data,
    ):
        item = cls.model(**data)
        logger.debug(item)
        db.add(item)
        await db.commit()
        return item

    @classmethod
    async def delete_item(
        cls,
        db: AsyncSession,
        item_id,
    ):
        stmt = delete(cls.model).where(cls.model.id == item_id)
        logger.debug(stmt)
        await db.execute(stmt)
        await db.commit()
