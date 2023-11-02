from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result


class BaseCRUD:
    model = None

    @classmethod
    async def get_item_by_id(
        cls,
        model_id: int,
        db: AsyncSession,
    ):
        model = await db.get(cls.model, model_id)
        return model

    @classmethod
    async def get_filtered_item(
        cls,
        db: AsyncSession,
        **filter_by,
    ):
        stmt = select(cls.model).filter_by(**filter_by)
        result: Result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_items(
        cls,
        db: AsyncSession,
        limit: int = 100,
    ):
        return db.query(cls.model).limit(limit).all()

    @classmethod
    async def add_item(
        cls,
        db: AsyncSession,
        **data,
    ):
        item = cls.model(**data)
        db.add(item)
        await db.commit()
