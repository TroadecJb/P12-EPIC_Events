import sqlalchemy
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from models.tables import Role, User
from controllers.db_manager import DatabaseManager
from controllers.authentication import Authentication_controller
from views.menu import Menu


def main():
    db_uri = "sqlite:///epic_events.sqlite"
    engine = create_engine(db_uri, echo=False)
    db_manager = DatabaseManager(engine, db_uri)
    db_manager.check_database()
    menu = Menu()
    auth_controller = Authentication_controller(engine)
    user_session = auth_controller.user_instance

    if user_session is None:
        credentials = menu.log_in()
        auth_controller.login(credentials[0], credentials[1])
        user_session = auth_controller.user_instance

    # with db_manager.session.begin() as session:
    #     stmt = select(User).where(User.email == "admin@mail.test")
    #     result = session.execute(stmt).first()
    #     print(result)


if __name__ == "__main__":
    main()
