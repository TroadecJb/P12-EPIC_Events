from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from controllers.permissions import Permission
from models.tables import User, Client, Contract, Event, Company, Address
from views.basic_view import (
    show,
    show_error_message,
    show_error_input,
    show_dict_kv,
    user_input,
)
from controllers import (
    actions_addresses,
    actions_clients,
    actions_companies,
    actions_contracts,
    actions_events,
    actions_users,
)

from controllers.actions_clients import ActionsClients


class ActionsManager:
    sale_actions = {}
    support_actions = {}
    manager_actions = {}
    admin_actions = {}

    def __init__(self, session, db_name, user):
        self.db_name = db_name
        self.session = session
        self.user = user
        self.permission = Permission()
        self.query = None
        self.user_permissions_level = user.role_id

    def table_selection(self, choice):
        pass

    def start(self):
        show("\n", 10 * "-", "Select the table", 10 * "-", "\n")

    def actions_choice(self):
        actions_dict = {
            1: "Clients",
            2: "Contracts",
            3: "Events",
            4: "Companies",
            5: "Addresses",
        }

        if self.user_permissions_level in [1, 2]:
            actions_dict[6] = "Users"
        else:
            pass

        show_dict_kv(actions_dict)
        choice = int(user_input())

        if int(choice) in actions_dict.keys():
            return self.table_selection(choice=int(choice))
        else:
            show_error_input()
            return self.actions_choice()
