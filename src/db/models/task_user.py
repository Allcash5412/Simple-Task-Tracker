from .base import Base

from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class TaskUser(Base):
    __tablename__ = 'task_user'

    task_id: Mapped[int] = mapped_column(ForeignKey('task.id'))
    user_id: Mapped[int] =  mapped_column(ForeignKey('user.id'))
