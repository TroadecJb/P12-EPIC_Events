import sqlalchemy
from sqlalchemy import create_engine, text
from models.users import User


def main():
    engine = create_engine("sqlite:///epic_events_sqla.db", echo=True)
    conn = engine.connect()
    metadata = sqlalchemy.MetaData()


main()

engine = create_engine("sqlite:///epic_events_sqla.db", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("Select 'hello world'"))
    print(result.all())
