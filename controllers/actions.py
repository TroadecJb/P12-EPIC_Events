from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from controllers.permissions import Permission
from models.tables import User, Client, Contract, Event, Company, Address


class db_actions:
    def __init__(self, session, db_name, user):
        self.db_name = db_name
        self.session = session
        self.user = user
        self.permission = Permission()
        self.query = None

    def read_clients_all(self):
        if self.permission.check(self.user, [1, 3, 4]):
            stmt = select(Client)
            result = self.session.scalars(stmt).all()
            return result
        else:
            return "t'as pas le droit"

    def read_clients_one_id(self, client_id):
        stmt = select(Client).where(Client.id == client_id)
        result = self.session.execute(stmt).first()
        return result

    def read_clients_one_name(self, client_name):
        stmt = select(Client).where(Client.name == client_name)
        result = self.session.execute(stmt).first()
        return result
