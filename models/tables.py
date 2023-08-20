from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, Boolean, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    contracts: Mapped[List["Contract"]] = relationship(back_populates="commercial")

    # def __repr__(self) -> str:
    #     return (
    #         f"id={self.id}, name={self.name}, role={self.role_id}, email={self.email}"
    #     )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f"id={self.id}, name={self.name}"


class Address(Base):
    """Class for address"""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(10))
    street: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    code: Mapped[int] = mapped_column(Integer)
    additionnal_info: Mapped[Optional[str]] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"id={self.id}, {self.number} {self.street} {self.code} {self.city}, {self.additionnal_info}"


class Client(Base):
    """Class for client"""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    contact_first: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    contact_last: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return (
            f"id={self.id}, name={self.name}, email={self.email}, phone={self.phone}."
        )


class Event(Base):
    """Class for event"""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    support_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_begin: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    date_end: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    number_attendee: Mapped[int] = mapped_column(Integer, default=0)
    note: Mapped[Optional[str]] = mapped_column(String(500), default="")

    def __repr__(self) -> str:
        return f"id={self.id}, contract_id={self.contract_id}, support_id={self.support_id}, addres_id={self.address_id}, date={self.date_begin} - {self.date_end}."


class Contract(Base):
    """Class for contract"""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["Client"] = relationship(back_populates="contracts")
    date_creation: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    cost_total: Mapped[float] = mapped_column(Float, default=0.0)
    cost_remaining: Mapped[float] = mapped_column(Float, default=cost_total)
    valid: Mapped[bool] = mapped_column(Boolean)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commercial: Mapped["User"] = relationship(back_populates="contracts")

    def __repr__(self) -> str:
        return f"id={self.id}, client_id={self.client_id}, commercial_id={self.commercial_id}, valid={self.valid}, cost={self.cost_total}, remaining={self.cost_remaining}."


class Company(Base):
    """Class for company"""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))

    def __repr__(self) -> str:
        return f"id={self.id}, name={self.name}, address_id={self.address_id}."
