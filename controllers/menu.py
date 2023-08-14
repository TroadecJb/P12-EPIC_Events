from utils.basic_utils import pwd_hashed
from views.basic_view import show, show_error_message, show_error_input, show_dict_kv
from controllers.actions import db_actions


class Menu:
    def __init__(self, user) -> None:
        self.user = user
        self.user_permissions_level = user.role_id

    user_permissions = {
        1: "admin",
        2: "manager",
        3: "sale",
        4: "support",
    }

    def start(self):
        show(10 * "#", self.__class__.__name__, 10 * "#")
        self.table_choice()

    def table_choice(self):
        print("\n- - -  Select action field - - -")
        tables_dict = {
            1: "Clients",
            2: "Contracts",
            3: "Companies",
            4: "Events",
            5: "Addresses",
        }

        if self.user_permissions_level in [1, 2]:
            tables_dict[6] = "\tUsers"
            show_dict_kv(tables_dict)

            choice = int(input("-> "))

            if 1 <= choice <= 6:
                return choice
            else:
                show_error_input()
                return self.table_choice()
        else:
            show_dict_kv(tables_dict)

            choice = int(input("-> "))

            if 1 <= choice <= 5:
                return choice
            else:
                show_error_input()
                return self.table_choice()
