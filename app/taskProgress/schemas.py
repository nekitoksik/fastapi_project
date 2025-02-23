from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserTaskProgressCreate(BaseModel):
    user_id: int
    task_id: int
    progress: int = 0

class UserTaskProgressUpdate(BaseModel):
    progress: int
    completed_at: Optional[datetime] = None

class SUserTaskProgress(BaseModel):
    id: int
    user_id: int
    task_id: int
    progress: int
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True