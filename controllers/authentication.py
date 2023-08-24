import bcrypt
import time
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models.tables import User, Role
from views.display import View

view = View()


class fg:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


class bg:
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    RESET = "\033[49m"


class other_style:
    BRIGHT = "\033[1m"
    DIM = "\033[2m"
    NORMAL = "\033[22m"
    RESET_ALL = "\033[0m"


class Authentication_controller:
    def __init__(self, session):
        self.session = session
        self.user_instance = None
        self.authentication_trials = 0

    def login(self):
        """Search in the database for a user with the proivided email, then check the password."""
        if self.authentication_trials >= 3:
            view.basic(f"{bg.RED}Too many attempts{bg.RESET}")
            time.sleep(3)
            quit()
        else:
            credentials = view.log_in()
            with self.session.begin() as session:
                stmt = select(User).where(User.email == credentials[0])
                result = session.execute(stmt).first()

                if result is not None and bcrypt.checkpw(
                    credentials[1], result.User.password
                ):
                    view.basic(f"\n{fg.GREEN}Connection success!{fg.RESET}")
                    view.basic(f"Welcome {result.User.name}!")
                    self.user_instance = User(
                        id=result.User.id,
                        name=result.User.name,
                        phone=result.User.phone,
                        email=result.User.email,
                        role_id=result.User.role_id,
                        role=result.User.role,
                    )
                    self.authentication_trials = 0
                    session.close()
                    return True

                elif result is not None and not bcrypt.checkpw(
                    credentials[1], result.User.password
                ):
                    view.error_message("invalid password.")
                    self.authentication_trials += 1
                    session.close()
                    return self.login()

                else:
                    view.error_message("invalid email.")
                    self.authentication_trials += 1
                    session.close()
                    return self.login()

    def logout(self):
        self.user_instance = None
        view.basic(f"{fg.GREEN}successfully logged out!{fg.RESET}")
