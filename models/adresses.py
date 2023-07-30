from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class address(Base):
    """Class for address"""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(10))
    street: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    code: Mapped[int] = mapped_column(Integer(10))
    additionnal_info: Mapped[Optional[str]] = mapped_column(String(100))

    def __init__(self) -> None:
        self.id = int()
        self.number = str()
        self.street = str()
        self.city = str()
        self.code = int()
        self.additionnal_info = str()
