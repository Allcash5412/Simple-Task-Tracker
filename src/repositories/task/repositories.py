import logging
from fastapi import HTTPException
from typing import Dict, Any, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.task_tracker.dto import CreateTask
from src.db.models import Task, TaskUser
from src.domain.task_tracker.entities import TaskBase
from src.services.task_tracker.interfaces import AbstractTaskRepository


logger = logging.getLogger('app')


class TaskRepository(AbstractTaskRepository):

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_task_model_by(self, filter_by: Dict[str, Any]) -> Optional[Task]:
        query = select(Task).filter_by(**filter_by)
        result = await self.session.execute(query)
        task = result.scalars().unique().first()
        return task

    async def get_task_by(self, filter_by: Dict[str, Any]) -> Optional[TaskBase]:
        task = await self.get_task_model_by(filter_by)
        return TaskBase.model_validate(task) if task else None

    async def update_task_by_id(self, task_id: int, data_for_update: Dict[str, Any]) -> None:
        logger.debug(f'task_id = {task_id}\n'
              f'data_for_update = {data_for_update}\n')
        try:
            assignees: Optional[Dict] = data_for_update.pop('assignees', None)

            if data_for_update:
                await self.session.execute(update(Task).where(Task.id == task_id).values(
                    **data_for_update))

            if assignees:
                await self.session.execute(
                    delete(TaskUser).where(TaskUser.task_id == task_id)
                )
                new_assignees = [
                    TaskUser(task_id=task_id, user_id=user.id) for user in assignees
                ]
                self.session.add_all(new_assignees)
        except Exception as e:
            await self.session.rollback()
            logger.error(e)
            raise HTTPException(status_code=500, detail='Task update error')

    async def create_task(self, task: CreateTask) -> TaskBase:
        try:
            new_task = Task(**task.__dict__)
            self.session.add(new_task)
            task: TaskBase = TaskBase.model_validate(new_task)
            return task
        except Exception as e:
            logger.error(e)

    async def delete_task_by(self, filter_by: Dict[str, Any]) -> None:
        await self.session.execute(delete(Task).filter_by(**filter_by))

    async def commit(self) -> None:
        await self.session.commit()

