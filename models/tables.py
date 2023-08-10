from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, Boolean
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

    def __repr__(self) -> str:
        return (
            f"id={self.id}, name={self.name}, role={self.role_id}, email={self.email}"
        )


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
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    contact_first: Mapped[str] = mapped_column(String)
    contact_last: Mapped[str] = mapped_column(String)
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
    date_begin: Mapped[datetime.datetime] = mapped_column(DateTime)
    date_end: Mapped[datetime.datetime] = mapped_column(DateTime)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    number_attendee: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"id={self.id}, contract_id={self.contract_id}, support_id={self.support_id}, addres_id={self.address_id}, date={self.date_begin} - {self.date_end}."


class Contract(Base):
    """Class for contract"""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    date_creation: Mapped[datetime.datetime] = mapped_column(DateTime)
    cost_total: Mapped[float] = mapped_column(Float)
    cost_remaining: Mapped[float] = mapped_column(Float)
    valid: Mapped[bool] = mapped_column(Boolean)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

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
