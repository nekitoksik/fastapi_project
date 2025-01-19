from fastapi import HTTPException
from app.tasks.models import Tasks
from app.services.base import BaseService

from app.tasks.schemas import STask

from app.database import async_session_maker
from sqlalchemy import select, delete

class TaskService(BaseService):
    model = Tasks

    @classmethod
    async def create_task(cls, task_data: STask) -> STask:
        async with async_session_maker() as session:
            db_task = Tasks(**task_data.model_dump(exclude_unset=True))
            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)
            return STask.model_validate(db_task)
    
    @classmethod
    async def delete_task(cls, task_id: int) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == task_id)
            await session.execute(query)
            await session.commit()

            try:
                get_task = select(cls.model.name).filter_by(id=task_id)
                get_task_result = await session.execute(get_task)
                raise HTTPException(status_code=500, detail="Задача не удалена")
            except:
                pass