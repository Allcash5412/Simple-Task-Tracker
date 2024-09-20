from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Task
from src.services.task_tracker.dto import CreateTask
from src.domain.task_tracker.entities import TaskBase


class AbstractAPICreateTask(ABC):
    name: str
    description: str
    responsible_person_id: int
    status: 'TaskStatus'
    priority: 'TaskPriority'
    assignees_ids: List[int]


class AbstractAPIUpdateTask(ABC):
    name: Optional[str]
    description: Optional[str]
    responsible_person_id: Optional[int]
    status: Optional['TaskStatus']
    priority: Optional['TaskPriority']
    assignees_ids: Optional[List[int]] = None



class AbstractTaskRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_task_by(self, filter_by: Dict[str, Any]) -> TaskBase:
        pass

    @abstractmethod
    async def get_task_model_by(self, filter_by: Dict[str, Any]) -> Optional[Task]:
        pass

    @abstractmethod
    async def update_task_by_id(self, task_id: int, data_for_update: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def create_task(self, user: CreateTask) -> TaskBase:
        pass

    @abstractmethod
    async def delete_task_by(self, filter_by: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
