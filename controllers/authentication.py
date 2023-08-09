import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models.tables import User
from views.basic_view import show_error, show


class Authentication_controller:
    def __init__(self, engine):
        self.session = sessionmaker(engine)
        self.user_instance = None

    def login(self, email, pwd):
        with self.session.begin() as session:
            stmt = select(User).where(User.email == email)
            result = session.execute(stmt).first()

            if result is not None and bcrypt.checkpw(pwd, result.User.password):
                show("Connection success!")
                self.user_instance = User(
                    id=result.User.id,
                    name=result.User.name,
                    phone=result.User.phone,
                    email=result.User.email,
                    role_id=result.User.role_id,
                )
                return True

            elif result is not None and not bcrypt.checkpw(pwd, result.User.password):
                show_error("invalid password.")
                return False

            else:
                show_error("invalid email.")
                return False

    def logout(self):
        self.user_instance = None
