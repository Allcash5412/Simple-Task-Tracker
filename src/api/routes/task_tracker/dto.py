from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.db.enums import TaskStatus, TaskPriority
from src.services.task_tracker.interfaces import AbstractAPICreateTask, AbstractAPIUpdateTask


class APICreateTask(BaseModel, AbstractAPICreateTask):
    name: str
    description: str
    responsible_person_id: int
    status: TaskStatus
    priority: TaskPriority
    assignees_ids: List[int]


class APIUpdateTask(BaseModel, AbstractAPIUpdateTask):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')

    name: Optional[str] = None
    description: Optional[str] = None
    responsible_person_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignees_ids: Optional[List[int]] = None
