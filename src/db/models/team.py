from typing import List

from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import BaseModel

class Team(BaseModel):
    """ Model for storing information about the team """
    __tablename__ = 'team'

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    users: Mapped[List['User']] = relationship(back_populates='team')
