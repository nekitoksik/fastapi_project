from sqlalchemy import select, update, delete
from fastapi import HTTPException
from app.database import async_session_maker
from app.taskProgress.models import UserTaskProgress
from app.taskProgress.schemas import SUserTaskProgress, UserTaskProgressCreate, UserTaskProgressUpdate

class UserTaskProgressService:
    @classmethod
    async def create_progress(cls, progress_data: UserTaskProgressCreate) -> SUserTaskProgress:
        async with async_session_maker() as session:
            db_progress = UserTaskProgress(**progress_data.model_dump())
            session.add(db_progress)
            await session.commit()
            await session.refresh(db_progress)
            return SUserTaskProgress.model_validate(db_progress)

    @classmethod
    async def update_progress(cls, progress_id: int, progress_data: UserTaskProgressUpdate) -> SUserTaskProgress:
        async with async_session_maker() as session:
            update_query = (
                update(UserTaskProgress)
                .where(UserTaskProgress.id == progress_id)
                .values(**progress_data.model_dump(exclude_unset=True))
            )
            await session.execute(update_query)
            await session.commit()

            get_progress_query = select(UserTaskProgress).where(UserTaskProgress.id == progress_id)
            result = await session.execute(get_progress_query)
            progress = result.scalar_one_or_none()

            if not progress:
                raise HTTPException(status_code=404, detail="Прогресс не найден")

            return SUserTaskProgress.model_validate(progress)

    @classmethod
    async def get_user_progresses(cls, user_id: int) -> list[UserTaskProgress]:
        async with async_session_maker() as session:
            query = select(UserTaskProgress).where(UserTaskProgress.user_id == user_id)
            result = await session.execute(query)
            progresses = result.scalars().all()
            return [SUserTaskProgress.model_validate(progress) for progress in progresses]

    @classmethod
    async def delete_progress(cls, progress_id: int) -> None:
        async with async_session_maker() as session:
            delete_query = delete(UserTaskProgress).where(UserTaskProgress.id == progress_id)
            await session.execute(delete_query)
            await session.commit()

    @classmethod
    async def get_task_progress(cls, user_id: int, task_id: int) -> UserTaskProgress:
        async with async_session_maker() as session:
            query = select(UserTaskProgress).where(
                UserTaskProgress.user_id == user_id,
                UserTaskProgress.task_id == task_id
            )
            result = await session.execute(query)
            progress = result.scalar_one_or_none()

            if not progress:
                raise HTTPException(status_code=404, detail="Прогресс не найден")

            return SUserTaskProgress.model_validate(progress)