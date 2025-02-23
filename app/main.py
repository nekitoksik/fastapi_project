from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import router as router_users
from app.tasks.router import router as router_tasks
from app.friendship.router import router as router_friendship
from app.runstats.router import router as router_runstats
from app.admins.router import router as router_admins
from app.taskProgress.router import router as router_taskProgress

app = FastAPI()


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cx54160.tw1.ru"],  # Укажите разрешенные источники (можно использовать ["*"] для всех)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(router_users)
app.include_router(router_tasks)
app.include_router(router_friendship)
app.include_router(router_runstats)
app.include_router(router_admins)
app.include_router(router_taskProgress)

app.mount("/images", StaticFiles(directory="images"), name="images")

