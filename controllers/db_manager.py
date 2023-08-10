from sqlalchemy import select, text, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from models.tables import Base, User, Role, Address, Client, Event, Company, Contract
from utils.basic_utils import pwd_hashed
from views.basic_view import show_error, show
from config_db_sqlalchemy import database_initialization


class DatabaseManager:
    def __init__(self, engine, db_name):
        self.db_name = db_name
        self.engine = engine
        self.session = sessionmaker(bind=engine)
        self.db_exist = False
        self.connection_trial = 0

    def check_database(self):
        if database_initialization(self.engine, self.db_name):
            self.db_exist = True

    def connection_close(self):
        if self.session is not None:
            self.session.close()
            show("connection closed")
