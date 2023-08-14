from sqlalchemy import select
from models.tables import User, Client, Contract, Event, Company, Address
from views.basic_view import show


class ActionsClients:
    def __repr__(self) -> str:
        return "Clients"

    def start(self):
        show("\n", 5 * "#", "Select whant you want to do", 5 * "#")
        actions = {
            1: self.read_clients,
            2: self.read_client_id,
            3: self.read_client_name,
        }

    def read_clients(session):
        stmt = select(Client)
        result = session.scalars(stmt).all()
        return result

    def read_client_id(session, client_id):
        stmt = select(Client).where(Client.id == client_id)
        result = session.execute(stmt).first()
        return result

    def read_client_name(session, client_name):
        stmt = select(Client).where(Client.name == client_name)
        result = session.execute(stmt).first()
        return result
