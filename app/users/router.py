from fastapi import APIRouter, Depends, UploadFile, File

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


@router.post("", response_model=SUserCreate, status_code=201)
async def create_user(user: SUserCreate):
    return await UserService.create_user(user)
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