from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.db.models import User
from src.db.enums import TaskStatus, TaskPriority


class CreateTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(max_length=150)
    description: str
    responsible_person: int
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    assignees: list[User]


class UpdateTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')

    name: Optional[str] = None
    description: Optional[str] = None
    responsible_person: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignees: Optional[list[User]] = None



class CreatedTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    name: str = Field(max_length=150)
    assignees: list[User]


class UpdatedTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    name: str = Field(max_length=150)
    responsible_person: Optional[User]
    assignees: Optional[list[User]]


class DeletedTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(max_length=150)
    assignees: list[User]

