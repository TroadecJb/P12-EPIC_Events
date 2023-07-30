from datetime import date
import datetime
from datetime import date
from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    """Class for client"""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    contact_first: Mapped[datetime.datetime] = mapped_column(date)
    contact_last: Mapped[datetime.datetime] = mapped_column(date)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __init__(self) -> None:
        """
        commercial_id: user_id
        """
        self.id = int()
        self.name = str()
        self.email = str()
        self.phone = str()
        self.first_contact = date()
        self.last_contact = date()
        self.company_id = int()
        self.commercial_id = int()
