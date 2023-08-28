from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, Boolean, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


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
    role: Mapped["Role"] = relationship(back_populates="users")
    contracts: Mapped[list["Contract"]] = relationship(
        back_populates="commercial", cascade="all, delete", passive_deletes=True
    )
    clients: Mapped[list["Client"]] = relationship(
        back_populates="commercial", cascade="all, delete", passive_deletes=True
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="support", cascade="all, delete", passive_deletes=True
    )

    def __str__(self) -> str:
        message = (
            f"id = {self.id}\n"
            f"name = {self.name}\n"
            f"role = {self.role.name}\n"
            f"email = {self.email}\n"
        )
        if self.contracts and self.clients:
            message += (
                f"contracts = {[(str(contract.client.name), str(contract.valid)) for contract in self.contracts]}\n"
                f"clients = {[str(client.name) for client in self.clients]}\n"
            )
        elif self.events:
            message += f"events = {[(str(event.contract.client.name), str(event.date_begin), str(event.date_end)) for event in self.events]}\n"
        else:
            pass
        return message

    def __repr__(self) -> str:
        return (
            f"id={self.id}, name={self.name}, email={self.name}, role={self.role.name}"
        )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __str__(self) -> str:
        message = f"id  = {self.id}\n" f"name  = {self.name}\n"
        return message

    def __repr__(self):
        return f"id={self.id}, name={self.name}"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    contracts: Mapped[list["Contract"]] = relationship(
        back_populates="client",
        cascade="all, delete",
        passive_deletes=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    contact_first: Mapped[date] = mapped_column(
        Date, server_default=func.current_date()
    )
    contact_last: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    company: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    address: Mapped[Optional[str]] = mapped_column(String(400), default=None)
    commercial_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    commercial: Mapped["User"] = relationship(back_populates="clients")

    def __str__(self) -> str:
        message = (
            f"name = {self.name}\n" f"email = {self.email}\n" f"phone = {self.phone}\n"
        )
        return message

    def __repr__(self) -> str:
        return f"id={self.id}, name={self.name}, phone={self.phone}, email={self.email}, commercial={str(self.commercial.name)} {str(self.commercial_id)}"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("contracts.id", ondelete="CASCADE")
    )
    contract: Mapped["Contract"] = relationship(back_populates="events")
    support_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    support: Mapped["User"] = relationship(back_populates="events")
    date_begin: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    date_end: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    address: Mapped[Optional[str]] = mapped_column(String(400), default=None)
    attendee: Mapped[int] = mapped_column(Integer, default=0)
    note: Mapped[Optional[str]] = mapped_column(String(500), default="")

    def __str__(self) -> str:
        message = (
            f"contract id = {self.contract_id}\n"
            f"contract = {str(self.contract.client.name)}\n"
            f"support = {str(self.support.name)}\n"
            f"date = {self.date_begin} - {self.date_end}\n"
        )
        return message

    def __repr__(self) -> str:
        return f"id={self.id}, contract={self.contract_id}, client={self.contract.client.name}, date={self.date_begin}-{self.date_end}"


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    client: Mapped["Client"] = relationship(back_populates="contracts")
    date_creation: Mapped[date] = mapped_column(
        Date, server_default=func.current_date()
    )
    cost_total: Mapped[float] = mapped_column(Float, default=0.0)
    cost_remaining: Mapped[float] = mapped_column(Float, default=cost_total)
    valid: Mapped[bool] = mapped_column(Boolean, default=False)
    commercial_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    commercial: Mapped["User"] = relationship(back_populates="contracts")
    events: Mapped[list["Event"]] = relationship(
        back_populates="contract",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self) -> str:
        message = (
            f"id =  {self.id}\n"
            f"client = {str(self.client.name)}\n"
            f"commercial = {str(self.commercial.name)}\n"
            f"valid = {self.valid}\n"
            f"cost = {self.cost_total}\n"
            f"remaining = {self.cost_remaining}\n"
        )
        return message

    def __repr__(self) -> str:
        return f"id={self.id}, client={self.client.name}, commercial={self.commercial.name} {self.commercial_id}, valid={self.valid}"
