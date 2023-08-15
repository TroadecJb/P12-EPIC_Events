import sqlalchemy
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from models.tables import Role, User
from controllers.db_manager import DatabaseManager
from controllers.authentication import Authentication_controller
from controllers.actions_tables import ActionsManager
from views.display import View


def main():
    db_uri = "sqlite:///epic_events_test.sqlite"
    engine = create_engine(db_uri, echo=False)
    db_manager = DatabaseManager(engine, db_uri)
    db_manager.check_database()
    auth_controller = Authentication_controller(engine)

    auth_controller.login()
    user_instance = auth_controller.user_instance
    session = sessionmaker(engine)

    # with session.begin() as sessionquimarche:
    menu = ActionsManager(session=session, user=user_instance)
    menu.start()

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
