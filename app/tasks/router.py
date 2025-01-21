from fastapi import APIRouter, Response

from app.tasks.schemas import STask, STaskCreate
from app.tasks.services import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=['Задачи'],
)

@router.get("")
async def get_tasks() -> list[STask]:
    result = await TaskService.get_all()

    return result

@router.post("", response_model=STaskCreate, status_code=201)
async def create_task(task: STaskCreate):
    return await TaskService.create_task(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    await TaskService.delete_task(task_id)
    return {}