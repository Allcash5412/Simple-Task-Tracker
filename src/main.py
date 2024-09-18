from fastapi import FastAPI

from src.api.routes.auth.router import auth as auth_router
from src.api.routes.task_tracker.router import task_tracker as task_tracker_router


app = FastAPI(root_path='/api/v1')


app.include_router(task_tracker_router, tags=['Task Tracker'])
app.include_router(auth_router, tags=['Auth'])
