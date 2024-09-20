from typing import List, Any, Optional

from pydantic import BaseModel, ConfigDict

from src.db.enums import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """ User entity """
    id: int | None = None
    name: str
    description: str
    responsible_person: Any
    status: TaskStatus
    priority: TaskPriority
    assignees: Optional[List[Any]]
    model_config = ConfigDict(from_attributes=True)
