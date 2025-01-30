from fastapi import APIRouter, Depends, UploadFile, File, Form

from typing import Optional
from app.users.schemas import SUser, SUserCreate
from app.users.services import UserService
from app.users.models import Users

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

@router.get("")
async def get_users() -> list[SUser]:
    result = await UserService.get_all()
    return result


@router.post("", response_model=SUser, status_code=201)
async def create_user(
    name: str = Form(...),
    height: int = Form(...),
    weight: int = Form(...),
    about: str = Form(...),
    city: str = Form(...),
    steps: int = Form(...),
    photo: UploadFile = File(None)
) -> SUser:
    user_data = SUserCreate(
        name=name,
        height=height,
        weight=weight,
        about=about,
        city=city,
        steps=steps
    )

    return await UserService.create_user(user_data, photo)
# @router.post("")
# async def create_user(
#     user: Users = Depends(),
#     photo: UploadFile = File(...),
# ):
#     return await UserService.create_user(user=user, photo=photo)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    await UserService.delete_user(user_id)
    return {}