from app.users.models import Users
from app.services.base import BaseService

from app.database import async_session_maker
from sqlalchemy import select

class UserService(BaseService):
    model = Users

    # @classmethod
    # async def get_user_by_id(cls, user_id: int) -> SUserSecure:
    #     async with async_session_maker() as session:
    #         query = select(cls.model.id, cls.model.email, cls.model.name).filter_by(id=user_id)
    #         result = await session.execute(query)
            
    #         user_data = result.fetchone()
    #         if user_data:
    #             return SUserSecure(id=user_data.id, email=user_data.email, name=user_data.name)  
    #         return None

    
