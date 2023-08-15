from sqlalchemy import select, update
from models.tables import User, Client, Contract, Event, Company, Address

from views.display import View

view = View()


def read_companies(session):
    with session.begin() as session:
        stmt = select(Company)
        result = session.scalars(stmt).all()
        return view.basic_list(result)


def read_company_by_id(session, company_id):
    with session.begin() as session:
        stmt = select(Company).where(Company.id == company_id)
        result = session.execute(stmt).first()
        return view.basic(result)


def read_company_by_name(session, company_name):
    with session.begin() as session:
        stmt = select(Company).where(Company.name == company_name)
        result = session.execute(stmt).first()
        return view.basic(result)
