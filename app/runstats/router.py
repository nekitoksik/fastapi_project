from fastapi import APIRouter

from app.runstats.schemas import SRunStats, SRunStatCreate
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

@router.post("/{user_id}/add_runstat")
async def add_new_runstat(user_id: int, run_data: SRunStatCreate):
    result = await RunStatsService.add_runstat(user_id=user_id, run_data=run_data)
    return result

@router.delete("/{runstat_id}", status_code=204)
async def delete_runstat(run_id: int):
    await RunStatsService.delete_runstat(run_id)