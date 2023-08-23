from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, Boolean, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


class fg:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


class bg:
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    RESET = "\033[49m"


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
    contracts: Mapped[list["Contract"]] = relationship(back_populates="commercial")
    clients: Mapped[list["Client"]] = relationship(back_populates="commercial")
    events: Mapped[list["Event"]] = relationship(back_populates="support")

    def __repr__(self) -> str:
        message = (
            f"{fg.MAGENTA}id {fg.RESET}= {self.id}\n"
            f"{fg.MAGENTA}name {fg.RESET}= {self.name}\n"
            f"{fg.MAGENTA}role{fg.RESET} = {self.role.name}\n"
            f"{fg.MAGENTA}email{fg.RESET} = {self.email}\n"
        )
        if self.contracts and self.clients:
            message += (
                f"{fg.MAGENTA}contracts {fg.RESET}= {[(contract.client.name, str(contract.valid)) for contract in self.contracts]}\n"
                f"{fg.MAGENTA}clients {fg.RESET}= {[client.name for client in self.clients]}\n"
            )
        elif self.events:
            message += f"{fg.MAGENTA}events {fg.RESET}= {[(event.contract.client.name, str(event.date_begin), str(event.date_end)) for event in self.events]}\n"
        else:
            pass
        return message


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        message = (
            f"{fg.MAGENTA}id {fg.RESET} = {self.id}\n"
            f"{fg.MAGENTA}name {fg.RESET} = {self.name}\n"
        )
        return message


class Client(Base):
    """Class for client"""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    contracts: Mapped[list["Contract"]] = relationship(back_populates="client")
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(100))
    contact_first: Mapped[date] = mapped_column(
        Date, server_default=func.current_date()
    )
    contact_last: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    company: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    address: Mapped[Optional[str]] = mapped_column(String(400), default=None)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commercial: Mapped["User"] = relationship(back_populates="clients")

    def __repr__(self) -> str:
        message = (
            f"{fg.MAGENTA}name {fg.RESET}= {self.name}\n"
            f"{fg.MAGENTA}email {fg.RESET}= {self.email}\n"
            f"{fg.MAGENTA}phone {fg.RESET}= {self.phone}\n"
        )
        return message


class Event(Base):
    """Class for event"""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    contract: Mapped["Contract"] = relationship(back_populates="events")
    support_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    support: Mapped["User"] = relationship(back_populates="events")
    date_begin: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    date_end: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    address: Mapped[Optional[str]] = mapped_column(String(400), default=None)
    number_attendee: Mapped[int] = mapped_column(Integer, default=0)
    note: Mapped[Optional[str]] = mapped_column(String(500), default="")

    def __repr__(self) -> str:
        message = (
            f"{fg.MAGENTA}contract id {fg.RESET}= {self.contract_id}\n"
            f"{fg.MAGENTA}contract {fg.RESET}= {self.contract.client.name}\n"
            f"{fg.MAGENTA}support {fg.RESET}= {self.support.name}\n"
            f"{fg.MAGENTA}date {fg.RESET}= {self.date_begin} - {self.date_end}\n"
        )
        return message


class Contract(Base):
    """Class for contract"""

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["Client"] = relationship(back_populates="contracts")
    date_creation: Mapped[date] = mapped_column(
        Date, server_default=func.current_date()
    )
    cost_total: Mapped[float] = mapped_column(Float, default=0.0)
    cost_remaining: Mapped[float] = mapped_column(Float, default=cost_total)
    valid: Mapped[bool] = mapped_column(Boolean, default=False)
    commercial_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commercial: Mapped["User"] = relationship(back_populates="contracts")
    events: Mapped[list["Event"]] = relationship(back_populates="contract")

    def __repr__(self) -> str:
        message = (
            f"{fg.MAGENTA}id {fg.RESET}=  {self.id}\n"
            f"{fg.MAGENTA}client {fg.RESET}= {self.client.name}\n"
            f"{fg.MAGENTA}commercial {fg.RESET}= {self.commercial.name}\n"
            f"{fg.MAGENTA}valid {fg.RESET}= {self.valid}\n"
            f"{fg.MAGENTA}cost {fg.RESET}= {self.cost_total}\n"
            f"{fg.MAGENTA}remaining {fg.RESET}= {self.cost_remaining}\n"
        )
        return message
