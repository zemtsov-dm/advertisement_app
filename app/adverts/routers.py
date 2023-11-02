from fastapi import APIRouter, Depends, status, HTTPException
from app.adverts.models import Advert

from app.users.models import User

# from ..dependences import get_current_admin_user, get_current_user
from .schemas import AdvertChange, AdvertCreate, AdvertResponse
from .crud import AdversCRUD
from sqlalchemy.ext.asyncio import AsyncSession

# from ..models import User
from app.database import get_session
from app.users.dependences import get_current_admin_user, get_current_user

router = APIRouter(
    prefix="/adverts",
    tags=["Adverts"],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_adverts(
    session: AsyncSession = Depends(get_session),
) -> list[AdvertResponse]:
    return await AdversCRUD.get_items(session)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_advert(
    data: AdvertCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = data.model_dump()
    data["owner_id"] = user.id
    return await AdversCRUD.add_item(session, **data)


@router.get("/{id}")
async def get_advert(
    id: int,
    session: AsyncSession = Depends(get_session),
) -> AdvertResponse:
    return await AdversCRUD.get_item_by_id(db =session,model_id=id)

@router.delete("/{id}")
async def delete_advert(
    id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    advert: Advert = await AdversCRUD.get_item_by_id(db=session,model_id=id)
    if advert.owner_id != user.id and user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await session.delete(advert)
    await session.commit()

@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def change_advert(
    id: int,
    data: AdvertChange,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_admin_user)
):
    advert: Advert = await AdversCRUD.get_item_by_id(db=session,model_id=id)
    advert.ad_type = data.ad_type
    await session.commit()
