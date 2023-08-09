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
            commercial = Role(name="commercial")
            manager = Role(name="manager")
            support = Role(name="support")

            pwd = bcrypt.hashpw(b"truc", bcrypt.gensalt())
            print(pwd)

            baseAdmin = User(
                name="admin",
                phone="",
                email="admin@mail.test",
                password=pwd,
                role_id=1,
            )

            session.add_all([admin, commercial, manager, support, baseAdmin])
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
