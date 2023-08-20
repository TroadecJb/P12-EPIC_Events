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
    session = sessionmaker(engine, expire_on_commit=False)

    # menu = ActionsManager(session=session, user=user_instance)
    # menu.start()
    # auth_controller = Authentication_controller(engine)
    # auth_controller.login()
    # user_instance = auth_controller.user_instance

    menu = ActionsManager(session=session)
    menu.signin()


if __name__ == "__main__":
    main()
