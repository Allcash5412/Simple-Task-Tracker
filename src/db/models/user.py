import datetime
from typing import List

from .base import BaseModel
from sqlalchemy import func, ForeignKey, Enum
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.sqlite import TIMESTAMP

from src.db.enums import UserRole


class User(BaseModel):
    """ Model for storing information about the user """
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    register_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=None)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.GUEST)
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('team.id'),
                                                    nullable=False)
    team: Mapped['Team'] = relationship(back_populates='users', lazy='joined')

    tasks: Mapped[List['Task']] = relationship(
        secondary='task_user',
        back_populates='assignees',
        lazy='joined'
    )
