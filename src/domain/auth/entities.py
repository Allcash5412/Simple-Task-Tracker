from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from src.db.enums import UserRole


class UserBase(BaseModel):
    """ User entity """
    id: int | None = None
    username: str
    password: str
    email: EmailStr
    register_at: datetime | None = None
    last_login: datetime | None = None
    role: UserRole = UserRole.USER
    team_id: Optional[int]
    team: Optional[str]
    tasks: Optional[List]

    model_config = ConfigDict(from_attributes=True)
