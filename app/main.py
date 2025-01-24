from fastapi import FastAPI

from app.users.router import router as router_users
from app.tasks.router import router as router_tasks
from app.friendship.router import router as router_friendship
from app.runstats.router import router as router_runstats

app = FastAPI()

app.include_router(router_users)
app.include_router(router_tasks)
app.include_router(router_friendship)
app.include_router(router_runstats)