from sqlalchemy import select, update
from models.tables import User, Client, Contract, Event, Company, Address

from views.display import View

view = View()


def read_events(session):
    stmt = select(Event)
    result = session.scalars(stmt).all()
    return view.basic_list(result)


def read_event_by_id(session, event_id):
    stmt = select(Event).where(Event.id == event_id)
    result = session.execute(stmt).first()
    return view.basic(result)


def read_event_by_name(session, event_name):
    stmt = select(Event).where(Event.name == event_name)
    result = session.execute(stmt).first()
    return view.basic(result)
