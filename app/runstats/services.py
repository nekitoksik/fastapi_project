from fastapi import HTTPException
from app.runstats.models import RunStats
from app.services.base import BaseService
from datetime import datetime
from app.runstats.schemas import SRunStats, SRunStatCreate

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
    

    @classmethod
    async def delete_runstat(cls, run_stat_id: int):
        async with async_session_maker() as session:
            runstat = await session.get(RunStats, run_stat_id)

            if not runstat:
                raise HTTPException(status_code=404, detail="User not found")

            delete_query = delete(cls.model).where(cls.model.id == run_stat_id)
            await session.execute(delete_query)
            await session.commit()
        
            return


    @classmethod
    async def add_runstat(cls, user_id: int, run_data: SRunStatCreate) -> RunStats:
        async with async_session_maker() as session:

            user = await session.get(Users, user_id)
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            start_datetime = datetime.combine(datetime.today(), run_data.start_time).replace(tzinfo=None)
            end_datetime = datetime.combine(datetime.today(), run_data.end_time).replace(tzinfo=None)

            time_difference = end_datetime - start_datetime

            time_in_hours = time_difference.total_seconds() / 3600

            if time_in_hours > 0:
                average_speed = run_data.distance / time_in_hours
            else:
                average_speed = 0.0
            
            new_run_stat = RunStats(
                user_id=user_id,
                distance=run_data.distance,
                start_time=start_datetime, 
                end_time=end_datetime, 
                steps=run_data.steps,
                calories_burned=run_data.calories_burned,
                average_speed=average_speed
            )
            
            session.add(new_run_stat)
            await session.commit()
            await session.refresh(new_run_stat)

            return new_run_stat
