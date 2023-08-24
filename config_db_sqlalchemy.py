from sqlalchemy.orm import sessionmaker
import bcrypt
from datetime import date

from models.tables import Base, User, Role, Client, Event, Contract
from views.display import View

from views.color import fg, bg

import configparser

config = configparser.ConfigParser()
config.read("config.txt")

view = View()


def database_initialization(engine, db):
    """
    Check if database exists by querying the rows of the roles tables.
    If the query is empty, the tables are created. Initializing the database.

    Args:
        engine : SQLAlchemy engine
        db (str) : address of the sqlite database

    Returns:
        (bool) : Database created/connected or Failure to do so
    """
    session = sessionmaker(engine)

    Base.metadata.create_all(engine)

    with session.begin() as session:
        message = f"{bg.YELLOW}Checking if {db} exists or not...{bg.RESET}"
        view.basic(message)
        check_empty = session.query(Role).first()

        if check_empty is None:
            view.basic(f"{fg.YELLOW}Database does not exist.{fg.RESET}")
            view.basic(f"{fg.YELLOW}Creating database: {db}{fg.RESET}")

            admin = Role(name="admin")
            sale = Role(name="sale")
            manager = Role(name="manager")
            support = Role(name="support")

            pwd = bcrypt.hashpw(
                config["admin_basic"]["password"].encode("utf-8"), bcrypt.gensalt()
            )

            baseAdmin = User(
                name="admin",
                phone="",
                email=config["admin_basic"]["email"],
                password=pwd,
                role_id=1,
            )

            session.add_all(
                [
                    admin,
                    manager,
                    sale,
                    support,
                    baseAdmin,
                ]
            )
            session.commit()

            view.basic(f"{bg.GREEN}Database created and initialized{bg.RESET}")
            session.close()
            return True

        elif check_empty is not None:
            view.basic(
                f"{bg.GREEN}Database exists. Succesfully connected to {db}{bg.RESET}"
            )
            session.close()
            return True
        else:
            view.error_message("Do some voodoo")
            session.close()
            return False
