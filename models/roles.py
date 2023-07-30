from abc import ABC, abstractmethod

from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))


class Commercial(ABC):
    """Class for commercial"""

    def commercial_test(self):
        print("i'm commercial")

    def client_create(self):
        """user is automatically set to client's contact (commercial_id)"""
        pass

    def client_update(self):
        """can update client(s) they are in charge of."""
        pass

    def event_create(self):
        pass

    def contract_update(self):
        """can update contract(s) they are in charge of."""
        pass

    def contract_filter_unvalid(self):
        pass

    def contract_filter_with_cost_remaining(self):
        pass


class Suppport(ABC):
    """Class for support"""

    def support_test(self):
        print("i'm support")

    def event_filter(self):
        """can filter event(s) they are in charge of."""
        pass

    def event_update(self):
        """can update event(s) they are in charge of."""
        pass


class Manager(ABC):
    """Class for manager"""

    def manager_test(self):
        print("i'm manager")

    def user_create(self):
        pass

    def user_update(self):
        pass

    def user_delete(self):
        pass

    def contract_create(self):
        """create contract(s)"""
        pass

    def contract_update(self):
        """update contract(s)"""
        pass

    def event_assign_support(self):
        """assign a support member to an event"""
        pass

    def event_filter_no_support_assigned(self):
        """can filter event(s) based on support assignment"""
        pass
