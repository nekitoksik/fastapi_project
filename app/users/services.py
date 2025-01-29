import os
from fastapi import HTTPException, UploadFile, File, Form
from PIL import Image
from pathlib import Path
from typing import Annotated
from app.users.models import Users
from app.services.base import BaseService

from app.users.schemas import SUser, SUserCreate
from typing import Annotated
from app.database import async_session_maker
from sqlalchemy import select, delete

IMAGE_DIR = "images/users"

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
    # async def create_user(
    #     avatar: Annotated[UploadFile, File(description="User avatar image")],
    #     name: Annotated[str, Form()],
    #     height: Annotated[int, Form()],
    #     weight: Annotated[int, Form()],
    #     about: Annotated[str, Form()],
    #     city: Annotated[str, Form()],
    #     steps: Annotated[int, Form()],
    # ) -> SUser:

    #     """Создает нового пользователя."""
    #     async with async_session_maker() as session:
    #         db_user = Users(
    #             name=name, 
    #             height=height, 
    #             weight=weight, 
    #             about=about, 
    #             city=city, 
    #             steps=steps
    #         )
    #         session.add(db_user)
    #         await session.commit()
    #         await session.refresh(db_user)

    #         if photo:
    #             Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

    #             try:
    #                 image = Image.open(photo.file)
    #                 file_extension = photo.filename.split(".")[-1].lower()
    #                 file_path = os.path.join(IMAGE_DIR, f"photo{db_user.id}.{file_extension}")

    #                 image.save(file_path)
    #                 db_user.photo_url = file_path

    #                 # Обновляем пользователя с добавленным фото
    #                 session.add(db_user)
    #                 await session.commit()
    #                 await session.refresh(db_user)

    #             except Exception as e:
    #                 print(f"Error saving image: {e}")
    #                 raise HTTPException(status_code=500, detail="Error saving image")

    #         return SUser.from_orm(db_user)
        





            # if photo:
            #     Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

            #     try:
            #         image = Image.open(photo.file)
            #         db_user = Users(**user_data.model_dump(exclude={"photo_url"}))
            #         session.add(db_user)
            #         await session.commit()
            #         await session.refresh(db_user)

            #         file_extension = photo.filename.split(".")[-1].lower()
            #         file_path = os.path.join(IMAGE_DIR, f"photo{db_user.id}.{file_extension}")

            #         image.save(file_path)

            #         db_user.photo_url = file_path
            #         await session.commit()
            #         await session.refresh(db_user)
                    
            #         return SUser.from_orm(db_user)
                
            #     except Exception as e:
            #         print(f"Error saving image: {e}")
            #         raise HTTPException(status_code=500, detail="Error saving image")
                
            # else:
            #     db_user = Users(**user_data.model_dump(exclude_unset=True))
            #     session.add(db_user)
            #     await session.commit()
            #     await session.refresh(db_user)

            # return SUser.model_validate(db_user)

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
