from pydantic import BaseModel
from datetime import time

class SRunStats(BaseModel):
    id: int
    time: time
    steps: int
    distance: float
    calories_burned: float
