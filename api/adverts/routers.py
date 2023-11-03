import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from api.adverts.filters import AdvertFilter
from api.adverts.models import Advert
from api.database import get_session
from api.users.dependences import (get_current_active_user,
                                   get_current_admin_user)
from api.users.models import User

from .crud import AdversCRUD
from .schemas import AdvertChange, AdvertCreate, AdvertResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/adverts",
    tags=["Adverts"],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[AdvertResponse])
async def get_adverts(
    session: AsyncSession = Depends(get_session),
    user_filter: AdvertFilter = FilterDepends(AdvertFilter),
):
    logger.info("Get all adverts")
    result = await AdversCRUD.get_items(
        db=session,
        user_filter=user_filter,
    )
    return result


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_advert(
    data: AdvertCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_active_user),
):
    logger.info("Create advert")
    data = data.model_dump()
    data["owner_id"] = user.id
    return await AdversCRUD.add_item(session, **data)


@router.get("/{id}")
async def get_advert(
    id: int,
    session: AsyncSession = Depends(get_session),
) -> AdvertResponse:
    logger.info("Get one advert")
    return await AdversCRUD.get_item_by_id(db=session, model_id=id)


@router.delete("/{id}")
async def delete_advert(
    id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_active_user),
):
    logger.info("Delete advert")
    advert: Advert = await AdversCRUD.get_item_by_id(db=session, model_id=id)
    if advert.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await session.delete(advert)
    await session.commit()


@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def change_advert(
    id: int,
    data: AdvertChange,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_admin_user),
):
    logger.info("Change advert")
    advert: Advert = await AdversCRUD.get_item_by_id(db=session, model_id=id)
    advert.ad_type = data.ad_type
    await session.commit()
