from sqlalchemy import select, update
from models.tables import User, Client, Contract, Event, Company, Address

from views.display import View

view = View()


def read_addresses(session):
    stmt = select(Address)
    result = session.scalars(stmt).all()
    return view.basic_list(result)


def read_address_by_id(session, address_id):
    stmt = select(Address).where(Address.id == address_id)
    result = session.execute(stmt).first()
    return view.basic(result)


def read_address_by_street(session, street_name):
    stmt = select(Address).where(Address.name == street_name)
    result = session.execute(stmt).all()
    return view.basic(result)


def read_address_by_code(session, code_name):
    stmt = select(Address).where(Address.code == code_name)
    result = session.execute(stmt).all()
    return view.basic(result)


def read_address_by_city(session, city_name):
    stmt = select(Address).where(Address.city == city_name)
    result = session.execute(stmt).all()
    return view.basic(result)
