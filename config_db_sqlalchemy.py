import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt
from datetime import date


from models.tables import Base, User, Role, Client, Event, Contract  # ,Address, Company
from views.display import View

view = View()


class fg:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


class bg:
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    RESET = "\033[49m"


class other_style:
    BRIGHT = "\033[1m"
    DIM = "\033[2m"
    NORMAL = "\033[22m"
    RESET_ALL = "\033[0m"


def database_initialization(engine, db):
    """
    Check if database exists by querying the rows of the roles tables.
    If the query is empty, the tables are created. Initializing the database.
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

            pwd = bcrypt.hashpw(b"truc", bcrypt.gensalt())

            test_client = Client(
                name="test_client",
                email="mail",
                phone="06",
                commercial_id=2,
            )
            test_client_2 = Client(
                name="test_client_2",
                email="mail",
                phone="07",
                commercial_id=2,
            )

            test_commerical = User(
                name="commercil",
                phone="",
                email="commercial@mail.test",
                password=pwd,
                role_id=3,
            )

            test_support = User(
                name="suppo",
                phone="",
                email="support@mail.test",
                password=pwd,
                role_id=4,
            )

            test_contract = Contract(
                client_id=1,
                date_creation=date(2020, 12, 20),
                cost_total=1000.5,
                cost_remaining=0.0,
                valid=True,
                commercial_id=2,
            )

            test_event = Event(
                contract_id=1,
                support_id=3,
                number_attendee=55,
            )

            baseAdmin = User(
                name="admin",
                phone="",
                email="admin@mail.test",
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
                    test_client,
                    test_client_2,
                    # test_company,
                    # test_address,
                    test_commerical,
                    test_support,
                    test_contract,
                    test_event,
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
