from sqlalchemy import select, update
from models.tables import User, Client, Contract, Event, Company, Address

from views.display import View

view = View()


def read_contracts(session):
    stmt = select(Contract)
    result = session.scalars().all()
    return view.basic_list(result)


def read_contract_by_id(session, contract_id):
    stmt = select(Contract).where(Contract.id == contract_id)
    result = session.execute(stmt).first()
    return view.basic(result)


def read_contract_by_name(session, contract_name):
    stmt = select(Contract).where(Contract.name == contract_name)
    result = session.execute(stmt).first()
    return view.basic(result)
