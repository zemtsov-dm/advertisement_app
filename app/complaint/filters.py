from fastapi_filter.contrib.sqlalchemy import Filter

from .models import Complaint

class ComplaintFilter(Filter):
    title__in: list[str] | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Complaint

