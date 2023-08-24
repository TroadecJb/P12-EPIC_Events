from sqlalchemy.orm import sessionmaker
from views.display import View
from config_db_sqlalchemy import database_initialization

view = View()


class DatabaseManager:
    def __init__(self, engine, db_name):
        self.db_name = db_name
        self.engine = engine
        self.session = sessionmaker(bind=engine)
        self.db_exist = False
        self.connection_trial = 0

    def check_database(self):
        """
        Check if the database exists or initializes it.

        Return:
            bool
        """
        if database_initialization(self.engine, self.db_name):
            self.db_exist = True
        else:
            return False

    def close_connection(self):
        if self.session is not None:
            self.session.close()
            View.basic("connection closed")
