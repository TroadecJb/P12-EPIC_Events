import sqlalchemy
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from models.tables import Role, User
from controllers.db_manager import DatabaseManager
from controllers.authentication import Authentication_controller
from controllers.actions import db_actions
from controllers.menu import Menu


def main():
    db_uri = "sqlite:///epic_events_test.sqlite"
    engine = create_engine(db_uri, echo=False)
    db_manager = DatabaseManager(engine, db_uri)
    db_manager.check_database()
    auth_controller = Authentication_controller(engine)
    user_session = None

    if user_session is None:
        if auth_controller.login():
            user_session = auth_controller.user_instance
        else:
            quit()

    menu = Menu(user_session)
    menu.table_choice()
    # session = sessionmaker(engine)
    # with session.begin() as sessionX:
    #     action = db_actions(sessionX, db_uri, user_session)
    #     print(action.read_clients_all())

    #     choice_id = int(input("enter id : "))
    #     choice_name = input("enter name : ")

    #     print(action.read_clients_one_id(choice_id))
    #     print(action.read_clients_one_name(choice_name))


if __name__ == "__main__":
    main()
