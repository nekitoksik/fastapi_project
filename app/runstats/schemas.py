from pydantic import BaseModel
from datetime import time

class SRunStats(BaseModel):
    id: int
    start_time: time
    end_time: time
    steps: int
    distance: float
    calories_burned: float

class SRunStatCreate(BaseModel):
    start_time: time
    end_time: time
    steps: int
    distance: float
    calories_burned: float
