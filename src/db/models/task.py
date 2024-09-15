from .base import BaseModel

from sqlalchemy import ForeignKey, BigInteger, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums import TaskStatus, TaskPriority


class Task(BaseModel):
    """ Model for storing information about the task """
    __tablename__ = 'task'

    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    responsible_person: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'),
                                                    nullable=False)

    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.MEDIUM)

    assignees: Mapped[list['User']] = relationship(
        secondary='task_user',
        back_populates='tasks',
        lazy='joined'
    )
