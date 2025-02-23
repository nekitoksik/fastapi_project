from fastapi import APIRouter, Response, UploadFile, File, Form

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

@router.post("", response_model=STask, status_code=201)
async def create_task(
    name: str = Form(...),
    task_type: str = Form(...),
    target_type: str = Form(...),
    target_value: int = Form(...),
    reward: int = Form(...),
    description: str = Form(...),
    photo: UploadFile = File(None)
) -> STask:
    task_data = STaskCreate(
        name=name,
        task_type=task_type,
        target_type=target_type,
        target_value=target_value,
        reward=reward,
        description=description
    )

    return await TaskService.create_task(task_data=task_data, photo=photo)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    await TaskService.delete_task(task_id)
    return {}