from app.crud.base import BaseCRUD
from app.core.models import User


class UserCRUD(BaseCRUD):
    model = User
