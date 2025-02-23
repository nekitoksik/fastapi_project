import os
import random
from typing import Optional
from jose import jwt, JWTError
from pathlib import Path
import requests
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, UploadFile, File, Form
from PIL import Image
from pathlib import Path

from app.users.models import Users
from app.services.base import BaseService
from app.config import settings

from app.users.schemas import SUser, SUserCreate, SUserUpdate
from app.database import async_session_maker
from sqlalchemy import select, delete

from app.exceptions import UserNotFoundException, InvalidSMSCodeException

IMAGE_DIR = "images/users"
SMSC_LOGIN = "bc100"
SMSC_PASSWORD = "Zyjxrf25!"

class UserService(BaseService):
    model = Users

    @classmethod
    async def create_user(cls, user_data: SUserCreate, photo: UploadFile = None) -> SUser:
        async with async_session_maker() as session:
            db_user = Users(**user_data.model_dump(exclude_unset=True))
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

            if photo:
                Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

                try:
                    image = Image.open(photo.file)
                    file_extension = photo.filename.split(".")[-1].lower()
                    file_path = os.path.join(IMAGE_DIR, f"photo{db_user.id}.{file_extension}")

                    image.save(file_path)
                    file_path = file_path.replace("\\", "/")
                    
                    db_user.photo_url = file_path
                    db_user.created_at = datetime.now()

                    session.add(db_user)
                    await session.commit()
                    await session.refresh(db_user)

                except Exception as e:
                    print(f"Error saving image: {e}")
                    raise HTTPException(status_code=500, detail="Error saving image")
                
            return SUser.model_validate(db_user)

    @classmethod
    async def update_user(
        cls,
        token: str,
        update_data: SUserUpdate
    ) -> Users:
 
        try:
            # Декодируем токен
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = int(payload.get("sub"))
            
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")

            async with async_session_maker() as session:
                # Находим пользователя
                result = await session.execute(
                    select(Users).where(Users.id == user_id)
                )
                user = result.scalar_one_or_none()

                if not user:
                    raise HTTPException(status_code=404, detail="User not found")

                # Обновляем поля
                update_dict = update_data.model_dump(exclude_unset=True)
                for field, value in update_dict.items():
                    setattr(user, field, value)

                session.add(user)
                await session.commit()
                await session.refresh(user)

                return user

        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    @classmethod
    async def upload_user_photo(
        cls,
        user: Users,
        photo: UploadFile
    ) -> SUser:
        async with async_session_maker() as session:
            try:
                if user.photo_url and user.photo_url != 'null_image.png':
                    old_path = Path(user.photo_url)
                    if old_path.exists():
                        old_path.unlink()

                Path(IMAGE_DIR).mkdir(exist_ok=True)
                image = Image.open(photo.file)
                file_extension = photo.filename.split('.')[-1].lower()
                file_path = os.path.join(IMAGE_DIR, f"photo{user.id}.{file_extension}")
                
                image.save(file_path)
                file_path = file_path.replace("\\", "/")

                user.photo_url = file_path
                
                session.add(user)
                await session.commit()
                await session.refresh(user)
                
                return SUser.model_validate(user)
                
            except Exception as e:
                print(f"Ошибка загрузки фото: {e}")
                raise HTTPException(500, "Ошибка обработки изображения")

    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        async with async_session_maker() as session:

            get_user_query = select(cls.model).where(cls.model.id == user_id)
            result = await session.execute(get_user_query)
            user = result.scalar_one_or_none()

            # query = delete(cls.model).where(cls.model.id == user_id)
            # await session.execute(query)
            # await session.commit()
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            
            photo_path = user.photo_url
            if photo_path:
                try:
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                except Exception as e:
                    print(f"Ошибка при удалении изображения: {e}")


            delete_query = delete(cls.model).where(cls.model.id == user_id)
            await session.execute(delete_query)
            await session.commit()

            return
    
    @classmethod
    async def add_points_to_user(cls, user_id: int, points_to_add: int) -> SUser:
        async with async_session_maker() as session:

            get_user_query = select(cls.model).where(cls.model.id == user_id)
            result = await session.execute(get_user_query)
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            
            user.points += points_to_add

            session.add(user)
            await session.commit()
            await session.refresh(user)

            return user

    @classmethod
    async def add_steps_to_user(cls, user_id: int, steps_to_add: int) -> SUser:
        async with async_session_maker() as session:

            get_user_query = select(cls.model).where(cls.model.id == user_id)
            result = await session.execute(get_user_query)
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            
            user.steps += steps_to_add

            session.add(user)
            await session.commit()
            await session.refresh(user)

            return user
        
    @classmethod
    async def send_verification_code(cls, phone: str):
        async with async_session_maker() as session:

            if phone == "77777777777":
                try:
                    user = await session.execute(select(Users).where(Users.phone_number == phone))
                    user = user.scalar_one_or_none()

                    code = '111111'
                    expires_at = datetime.now() + timedelta(minutes=5) 
                    
                    if user:
                        user.verification_code = code
                        user.code_expires_at = expires_at
                    
                    else:
                        user = Users(
                            phone_number=phone,
                            verification_code=code,
                            code_expires_at=expires_at
                        )

                    session.add(user)
                    await session.commit()
                    return {"status": "Код отправлен"}
                
                except Exception as e:
                    print(f"Ошибка {e}")
                    raise HTTPException(500, "Ошибка при создании кода для тестового пользователя") 



            else:
                user = await session.execute(select(Users).where(Users.phone_number == phone))
                user = user.scalar_one_or_none()

                code = str(random.randint(100000, 999999))
                expires_at = datetime.now() + timedelta(minutes=5)

                if user:
                    user.verification_code = code
                    user.code_expires_at = expires_at
                
                else:
                    user = Users(
                        phone_number=phone,
                        verification_code=code,
                        code_expires_at=expires_at
                    )

                session.add(user)
                await session.commit()

                response = requests.get(
                    "https://smsc.ru/sys/send.php",
                    params={
                        "login": SMSC_LOGIN,
                        "psw": SMSC_PASSWORD,
                        "phones": phone,
                        "mes": f"Ваш код подтверждения: {code}",
                        "fmt": 3
                    }
                )

                if response.json().get("error"):
                    raise Exception("Ошибка отправки SMS")

                return {"status": "Код отправлен"}

            


    @classmethod
    async def verify_code(cls, phone: str, code: str):
        async with async_session_maker() as session:
            user = await session.execute(select(Users).where(Users.phone_number == phone))
            user = user.scalar_one_or_none()

            if not user:
                raise UserNotFoundException

            if user.verification_code != code:
                raise InvalidSMSCodeException

            if datetime.now() > user.code_expires_at:
                raise InvalidSMSCodeException("Код устарел")

            token = jwt.encode(
                {"sub": str(user.id)},
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM
            )

            user.jwt_token = token
            session.add(user)
            await session.commit()

            return {"access_token": token, "token_type": "bearer"} 
        
    @classmethod
    async def logout_user(cls, current_user: Users):
        async with async_session_maker() as session:
            current_user.jwt_token = None
            session.add(current_user)
            await session.commit()

    @classmethod
    async def check_phone_unique(cls, phone_number: str) -> bool:
        async with async_session_maker() as session:
            existing_user = await session.execute(
                select(Users).where(Users.phone_number == phone_number)
            )
            existing_user = existing_user.scalar_one_or_none()

            # Если пользователь не существует или он "пустой" (с именем "Новый пользователь")
            if existing_user is None or existing_user.name == "Новый пользователь":
                return True

            return False