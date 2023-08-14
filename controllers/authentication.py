import bcrypt
import time
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models.tables import User
from views.basic_view import show_error, show, log_in


class Authentication_controller:
    def __init__(self, engine):
        self.session = sessionmaker(engine)
        self.user_instance = None
        self.authentication_trials = 0

    def login(self):
        """Search in the database for a user with the proivided email, then check the password."""
        if self.authentication_trials > 3:
            show_error("Too many attempts.")
            time.sleep(3)
            return False

        credentials = log_in()
        with self.session.begin() as session:
            stmt = select(User).where(User.email == credentials[0])
            result = session.execute(stmt).first()

            if result is not None and bcrypt.checkpw(
                credentials[1], result.User.password
            ):
                show(f"\nConnection success!\nWelcome {result.User.name}!")
                self.user_instance = User(
                    id=result.User.id,
                    name=result.User.name,
                    phone=result.User.phone,
                    email=result.User.email,
                    role_id=result.User.role_id,
                )
                self.authentication_trials = 0
                return True

            elif result is not None and not bcrypt.checkpw(
                credentials[1], result.User.password
            ):
                show_error("invalid password.")
                self.authentication_trials += 1
                return self.login()

            else:
                show_error("invalid email.")
                return self.login()

    def logout(self):
        self.user_instance = None
