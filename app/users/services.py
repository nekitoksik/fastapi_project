from fastapi import HTTPException
from app.users.models import Users
from app.services.base import BaseService

from app.users.schemas import SUser, SUserCreate

from app.database import async_session_maker
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

class UserService(BaseService):
    model = Users

    @classmethod
    async def create_user(cls, user_data: SUserCreate) -> SUser:
        """Создает нового пользователя."""
        async with async_session_maker() as session:
            db_user = Users(**user_data.model_dump(exclude_unset=True))
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return SUser.model_validate(db_user)

    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == user_id)
            await session.execute(query)
            await session.commit()

            try:
                get_user = select(cls.model.name).filter_by(id=user_id)
                get_user_result = await session.execute(get_user)
                raise HTTPException(status_code=500, detail="Пользователь не удален")
            except:
                pass


    @classmethod
    async def get_friends_by_id(cls, user_id: int) -> list[dict]:
        async with async_session_maker() as session:
            user = await session.get(cls.model, user_id, options=[selectinload(cls.model.friends)])
            if not user:
                return []
        
        friends_data = []
        for friend in user.friends:
            friends_data.append({"id": friend.id, "name": friend.name, "steps": friend.steps})

        return friends_data