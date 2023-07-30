import datetime
from datetime import date

from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Contract(Base):
    """Class for contract"""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    date_creation: Mapped[datetime.datetime] = mapped_column(date)
    cost_total: Mapped[float] = mapped_column(Float)
    cost_remaining: Mapped[float] = mapped_column(Float)
    valid: Mapped[bool] = mapped_column(Boolean)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __init__(self) -> None:
        """
        commercial_id: user_id
        """
        self.id = int()
        self.client_id = int()
        self.date_creation = date()
        self.cost_total = float()
        self.cost_remaining = float()
        self.valid = bool()
        self.commercial_id = int()
