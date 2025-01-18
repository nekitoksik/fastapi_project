from fastapi import APIRouter, Response

from app.users.schemas import SUser
from app.users.services import UserService

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

@router.get("")
async def get_users() -> list[SUser]:
    result = await UserService.get_all()

    return result