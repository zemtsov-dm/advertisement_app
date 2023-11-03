from api.base_crud import BaseCRUD
from .models import User

class UserCRUD(BaseCRUD):
    model = User