from fastapi_filter.contrib.sqlalchemy import Filter

from app.users.models import User 

class UserFilter(Filter):
    name__in: list[str] | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = User
