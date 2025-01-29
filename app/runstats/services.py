from fastapi import HTTPException
from app.runstats.models import RunStats
from app.services.base import BaseService

from app.runstats.schemas import SRunStats

from app.database import async_session_maker
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.users.models import Users

class RunStatsService(BaseService):
    model = RunStats

    @classmethod
    async def get_all_runstats(cls, user_id: int):
        async with async_session_maker() as session:
            user = await session.get(Users, user_id)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")
                        
            query = select(RunStats).filter(RunStats.user_id == user_id)
            result = await session.execute(query)
        
            return result.scalars().all()
        
    # @classmethod
    # async def add_runstat(cls, run_data: )