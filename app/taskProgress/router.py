from fastapi import APIRouter, Depends, HTTPException
from app.taskProgress.services import UserTaskProgressService
from app.taskProgress.schemas import UserTaskProgressCreate, UserTaskProgressUpdate, SUserTaskProgress

router = APIRouter(
    prefix="/user-task-progress",
    tags=["Прогресс Задач"],
)

@router.post("", response_model=SUserTaskProgress, status_code=201)
async def create_progress(progress_data: UserTaskProgressCreate):
    return await UserTaskProgressService.create_progress(progress_data)

@router.put("/{progress_id}", response_model=SUserTaskProgress)
async def update_progress(progress_id: int, progress_data: UserTaskProgressUpdate):
    return await UserTaskProgressService.update_progress(progress_id, progress_data)

@router.get("/user/{user_id}", response_model=list[SUserTaskProgress])
async def get_user_progresses(user_id: int):
    return await UserTaskProgressService.get_user_progresses(user_id)

@router.delete("/{progress_id}", status_code=204)
async def delete_progress(progress_id: int):
    await UserTaskProgressService.delete_progress(progress_id)
    return {}

@router.get("/user/{user_id}/task/{task_id}", response_model=SUserTaskProgress)
async def get_task_progress(user_id: int, task_id: int):
    return await UserTaskProgressService.get_task_progress(user_id, task_id)