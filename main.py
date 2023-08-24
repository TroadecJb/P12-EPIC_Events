from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.db_manager import DatabaseManager
from controllers.actions_tables import ActionsManager
import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import configparser

config = configparser.ConfigParser()
config.read("config.txt")


def main():
    sentry_sdk.init(
        dsn=config["config"]["sentry_dsn"],
        integrations=[
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=1.0,
    )

    db_uri = config["config"]["db"]
    engine = create_engine(db_uri, echo=False)
    db_manager = DatabaseManager(engine, db_uri)
    db_manager.check_database()
    session = sessionmaker(engine, expire_on_commit=False)

    menu = ActionsManager(session=session)
    menu.signin()


if __name__ == "__main__":
    main()
