from fastapi import APIRouter

from app.runstats.schemas import SRunStats
from app.runstats.models import RunStats
from app.runstats.services import RunStatsService

router = APIRouter(
    prefix="/runstats",
    tags=["Забеги"],
)

@router.get("/{user_id}")
async def get_runstats(user_id: int):
    result = await RunStatsService.get_all_runstats(user_id)
    return result