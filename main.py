import sqlalchemy
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from models.tables import Role, User
from controllers.db_manager import DatabaseManager
from controllers.authentication import Authentication_controller
from controllers.actions import db_actions
from views.menu import Menu


def main():
    db_uri = "sqlite:///epic_events_test.sqlite"
    engine = create_engine(db_uri, echo=False)
    db_manager = DatabaseManager(engine, db_uri)
    db_manager.check_database()
    menu = Menu()
    auth_controller = Authentication_controller(engine)
    user_session = auth_controller.user_instance

    if user_session is None:
        credentials = menu.log_in()
        if auth_controller.login(credentials[0], credentials[1]):
            user_session = auth_controller.user_instance
        else:
            quit()

    # with db_manager.session.begin() as session:
    #     stmt = select(User).where(User.email == "admin@mail.test")
    #     result = session.execute(stmt).first()
    #     print(result)

    # test connection et accès DB avec permission
    session = sessionmaker(engine)
    with session.begin() as sessionX:
        action = db_actions(sessionX, db_uri, user_session)
        print(action.read_clients_all())

        choice_id = int(input("enter id : "))
        choice_name = input("enter name : ")

        print(action.read_clients_one_id(choice_id))
        print(action.read_clients_one_name(choice_name))


if __name__ == "__main__":
    main()
