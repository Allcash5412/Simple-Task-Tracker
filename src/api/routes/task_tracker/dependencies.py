from typing import Annotated

from fastapi import Depends

from src.repositories.task.repositories import TaskRepository
from src.api.routes.dependencies import SessionDep


def get_task_repository(session: SessionDep) -> TaskRepository:
    return TaskRepository(session)


TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
