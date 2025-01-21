from fastapi import APIRouter, Response

from app.users.schemas import SUser, SUserCreate
from app.users.services import UserService

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


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    await UserService.delete_user(user_id)
    return {}


@router.get("/friends/{user_id}")
async def get_user_friends(user_id: int):
    result = await UserService.get_friends_by_id(user_id)

    return result