import logging
from fastapi import APIRouter, Depends, status
from api.users.models import User
from fastapi_pagination import Page
from .filters import ComplaintFilter
from . import schemas
from .crud import ComplaintCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends
from api.database import get_session
from api.users.dependences import get_current_admin_user, get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/adverts/{advert_id}/complaints",
    tags=["Complaints"],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[schemas.ComplaintResponseSchema])
async def get_complaints(
    advert_id: int,
    session: AsyncSession = Depends(get_session),
    user_filter: ComplaintFilter = FilterDepends(ComplaintFilter),
    user: User = Depends(get_current_admin_user),
):
    logger.info("Get complaints")
    result = await ComplaintCRUD.get_items(
        advert_id,
        db=session,
        user_filter=user_filter,
    )
    return result


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_complaint(
    advert_id:int,
    data: schemas.ComplaintCreateSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_active_user),
):
    logger.info("Create complaint")
    data = data.model_dump()
    data["user_id"] = user.id
    data["advert_id"] = advert_id 
    return await ComplaintCRUD.add_item(session, **data)


@router.get("/{complaint_id}")
async def get_compalint(
    advert_id: int,
    complaint_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_admin_user),
) -> schemas.ComplaintResponseSchema:
    logger.info(f"Get complaint witn id {complaint_id}")
    return await ComplaintCRUD.get_item_by_id(db=session, model_id=id)