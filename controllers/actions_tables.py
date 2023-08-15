from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from controllers.permissions import Permission
from models.tables import User, Client, Contract, Event, Company, Address
from views.display import View


from controllers import (
    actions_clients,
    actions_contracts,
    actions_events,
    actions_companies,
    actions_addresses,
    actions_users,
)

view = View()


class ActionsManager:
    actions_by_role = {
        1: {
            1: actions_clients.read_clients,
            2: actions_clients.read_client_by_name,
            3: actions_clients.update_client_by_name,
            4: actions_companies.read_companies,
        },
        2: {},
        3: {},
        4: {},
    }

    def __init__(self, session, user):
        self.name = "what do you want to do"
        # self.db_name = db_name
        self.session = session
        self.user = user
        self.user_permissions_level = user.role_id
        self.actions_dict = self.actions_by_role[self.user_permissions_level]
        self.permission = Permission()
        self.query = None

    def start(self):
        view.menu_name(self.name)
        view.dict_kv_func(self.actions_dict)
        choice = int(view.user_input())

        if choice in self.actions_dict.keys():
            self.actions_dict[choice](self.session)
        else:
            view.error_input()
        return self.start()
