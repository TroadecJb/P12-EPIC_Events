import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt


from models.tables import Base, User, Role, Address, Client, Event, Company, Contract
from views.display import View

view = View()


def database_initialization(engine, db):
    """
    Check if database exists by querying the rows of the roles tables.
    If the query is empty, the tables are created. Initializing the database.
    """
    session = sessionmaker(engine)

    Base.metadata.create_all(engine)

    with session.begin() as session:
        message = f"Checking if {db} exists or not..."
        view.basic(message)
        check_empty = session.query(Role).first()

        if check_empty is None:
            view.basic(f"Database does not exist.")
            view.basic(f"Creating database: {db}")

            admin = Role(name="admin")
            sale = Role(name="sale")
            manager = Role(name="manager")
            support = Role(name="support")

            pwd = bcrypt.hashpw(b"truc", bcrypt.gensalt())

            test_client = Client(
                name="test_client",
                email="mail",
                phone="06",
                contact_first="hier",
                contact_last="aujourd'hui",
                company_id=1,
                commercial_id=2,
            )
            test_client_2 = Client(
                name="test_client_2",
                email="mail",
                phone="07",
                contact_first="hier",
                contact_last="aujourd'hui",
                company_id=1,
                commercial_id=2,
            )

            test_company = Company(
                name="test_company",
                address_id=1,
            )

            test_address = Address(
                number="1",
                street="rue",
                city="ville",
                code=22,
            )

            test_commerical = User(
                name="commercil",
                phone="",
                email="commercial@mail.test",
                password=pwd,
                role_id=3,
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
                    test_company,
                    test_address,
                    test_commerical,
                ]
            )
            session.commit()

            view.basic(f"Database created and initialized.")
            session.close()
            return True

        elif check_empty is not None:
            view.basic(f"Database exists. Succesfully connected to {db}.")
            session.close()
            return True
        else:
            view.error_message("Do some voodoo")
            session.close()
            return False
