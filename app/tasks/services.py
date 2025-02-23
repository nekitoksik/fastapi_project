import os
from datetime import datetime
from fastapi import HTTPException, UploadFile
from app.tasks.models import Tasks
from app.services.base import BaseService
from PIL import Image
from typing import Annotated
from pathlib import Path
from app.tasks.schemas import STask, STaskCreate

from app.database import async_session_maker
from sqlalchemy import select, delete

IMAGE_DIR = "images/tasks"

class TaskService(BaseService):
    model = Tasks

    @classmethod
    async def create_task(cls, task_data: STaskCreate, photo: UploadFile = None) -> STask:
        async with async_session_maker() as session:
            db_task = Tasks(**task_data.model_dump(exclude_unset=True))
            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)

            if photo:
                Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

                try:
                    image = Image.open(photo.file)
                    file_extension = photo.filename.split(".")[-1].lower()
                    file_path = os.path.join(IMAGE_DIR, f"photo{db_task.id}.{file_extension}")

                    image.save(file_path)
                    file_path = file_path.replace("\\", "/")
                    
                    db_task.image_path = file_path

                    session.add(db_task)
                    await session.commit()
                    await session.refresh(db_task)

                except Exception as e:
                    print(f"Error saving image: {e}")
                    raise HTTPException(status_code=500, detail="Error saving image")

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