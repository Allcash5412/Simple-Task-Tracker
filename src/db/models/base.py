from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    """ Base model """

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, 'sqlite'),
                                    primary_key=True)