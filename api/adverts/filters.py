from fastapi_filter.contrib.sqlalchemy import Filter

from api.adverts.models import Advert


class AdvertFilter(Filter):
    title__in: list[str] | None = None
    price__gt: int | None = None
    price__lt: int | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Advert
