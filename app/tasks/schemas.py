from pydantic import BaseModel

class STask(BaseModel):
    id: int
    task_type: str
    name: str
    target_type: str
    target_value: int
    reward: int
    description: str
    image_path: str
    

    class Config:
        from_attributes = True

class STaskCreate(BaseModel):
    task_type: str
    name: str
    target_type: str
    target_value: int
    reward: int
    description: str
    image_path: str
