from app.admins.models import Admins
from app.services.base import BaseService

from app.database import async_session_maker
from sqlalchemy import select

class AdminService(BaseService):
    model = Admins
