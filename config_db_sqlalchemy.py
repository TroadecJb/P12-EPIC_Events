import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt


from models.tables import Base, User, Role, Address, Client, Event, Company, Contract
from views.basic_view import show_error, show


def database_initialization(engine, db):
    # engine = create_engine(db, echo=False)
    # # conn = engine.connect()
    # # metadata = sqlalchemy.MetaData()
    session = sessionmaker(engine)

    Base.metadata.create_all(engine)

    with session.begin() as session:
        show(f"Checking if {db} exists or not...")
        check_empty = session.query(Role).first()

        if check_empty is None:
            show(f"Database does not exist.")
            show(f"Creating database: {db}")

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
                role_id=2,
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
                    sale,
                    manager,
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

            show(f"Database created and initialized.")
            session.close()
            return True

        elif check_empty is not None:
            show(f"Database exists. Succesfully connected to {db}.")
            session.close()
            return True
        else:
            show_error("Do some voodoo")
            session.close()
            return False
