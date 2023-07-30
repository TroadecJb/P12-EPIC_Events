from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    """Class for company"""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))

    def __init__(self) -> None:
        self.id = int()
        self.name = str()
        self.address_id = int()
