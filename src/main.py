from fastapi import FastAPI

from src.api.routes.auth.router import auth as auth_router
from src.api.routes.task_tracker.router import task_tracker as task_tracker_router

api_description = ('API Description: When a user is created, he is given the role: USER,\n'
                   'For now, they can only be changed through the database.\n'
                   'Each endpoint has a list of allowable roles.\n'
                   'Correct execution of Task Tracker endpoints returns the name of the task')
app = FastAPI(root_path='/api/v1', description=api_description)


app.include_router(task_tracker_router, tags=['Task Tracker'])
app.include_router(auth_router, tags=['Auth'])
