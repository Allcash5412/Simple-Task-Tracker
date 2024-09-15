from src.db.database import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel(Base):
    """Base class for all models"""
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
