from fastapi import APIRouter, Response

from app.users.schemas import SUser, SUserCreate
from app.users.services import UserService

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker

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