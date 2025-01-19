from fastapi import FastAPI

from app.users.router import router as router_users
from app.tasks.router import router as router_tasks

app = FastAPI()

app.include_router(router_users)
app.include_router(router_tasks)