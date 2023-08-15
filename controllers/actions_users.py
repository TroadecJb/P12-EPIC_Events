from sqlalchemy import select, update
from models.tables import User, Client, Contract, Event, Company, Address

from views.display import View

view = View()


def read_users(session):
    stmt = select(User)
    result = session.scalars(stmt).all()
    return view.basic_list(result)


def read_user_by_id(session, user_id):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt).first()
    return view.basic(result)


def read_user_by_name(session, user_name):
    stmt = select(User).where(User.name == user_name)
    result = session.execute(stmt).first()
    return view.basic(result)


def read_user_by_email(session, user_email):
    stmt = select(User).where(User.email == user_email)
    result = session.execute(stmt).first()
    return view.basic(result)


def read_user_by_phone(session, user_phone):
    stmt = select(User).where(User.phone == user_phone)
    result = session.execute(stmt).first()
    return view.basic(result)
