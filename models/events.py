import datetime
from datetime import date

from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Event(Base):
    """Class for event"""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    support_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_begin: Mapped[datetime.datetime] = mapped_column(date)
    date_end: Mapped[datetime.datetime] = mapped_column(date)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    number_attendee: Mapped[int] = mapped_column(Integer(10000))
    note: Mapped[str] = mapped_column(String(500))

    def __init__(self) -> None:
        """
        support_id: user_id
        """
        self.id = int()
        self.contract_id = int()
        self.support_id = int()
        self.date_begin = date()
        self.date_end = date()
        self.address_id = int()
        self.number_attendee = int()
        self.note = str()
