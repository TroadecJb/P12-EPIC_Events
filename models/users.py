from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    def __init__(self) -> None:
        self.id = int()
        self.name = str()
        self.email = str()
        self.phone = str()
        self.role_id = int()

    def __repr__(self):
        return f"User(id={self.id}), name={self.name}"

    def user_test(self):
        print("i'm user")

    def change_password(self):
        pass

    def client_read(self):
        pass

    def contract_read(self):
        pass

    def event_read(self):
        pass

    def company_read(self):
        pass

    def address_read(self):
        pass

    def address_create(self):
        pass

    def address_update(self):
        pass
