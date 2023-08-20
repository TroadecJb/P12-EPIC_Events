from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from controllers.permissions import Permission
from models.tables import User, Client, Contract, Event, Company, Address
from views.display import View

from controllers.authentication import Authentication_controller


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
    actions_admin = {
        "logout": "",
        "clients": {
            1: actions_clients.read_clients,
            2: actions_clients.create_client,
            3: actions_clients.update_client,
            4: actions_clients.delete_client,
        },
        "contracts": {
            1: actions_contracts.read_contract,
        },
        "events": {
            1: actions_events.read_event,
        },
        "users": {1: actions_users.read_users},
    }
    actions_manager = {
        "logout": "",
        "clients": {
            1: actions_clients.read_clients,
        },
        "contracts": {
            1: actions_contracts.read_contract,
            2: actions_contracts.create_contract,
            3: actions_contracts.update_contract,
        },
        "events": {
            1: actions_events.read_event,
            2: actions_events.update_event,
        },
        "users": {
            1: actions_users.read_users,
            2: actions_users.create_user,
            3: actions_users.update_user,
            4: actions_users.delete_user,
        },
    }
    actions_sale = {
        "logout": "",
        "clients": {
            1: actions_clients.read_clients,
            2: actions_clients.create_client,
            3: actions_clients.update_client_in_charge,
        },
        "contracts": {
            1: actions_contracts.read_contract,
            2: actions_contracts.update_contract_in_charge,
        },
        "events": {
            1: actions_events.read_event,
            2: actions_events.create_event,
        },
    }
    action_support = {
        "logout": "",
        "clients": {
            1: actions_clients.read_clients,
        },
        "contracts": {
            1: actions_contracts.read_contract,
        },
        "events": {
            1: actions_events.read_events,
            2: actions_events.read_events_in_charge,
            3: actions_events.update_event_in_charge,
        },
    }

    actions_by_role = {
        1: actions_admin,
        2: actions_manager,
        3: actions_sale,
        4: action_support,
    }

    def __init__(self, session):
        self.auth_controller = Authentication_controller(session)

        self.name = "what do you want to do"
        self.session = session
        # self.user = self.auth_controller.user_instance
        # self.user_permissions_level = self.user.role_id
        # self.actions_dict = self.actions_by_role[self.user_permissions_level]
        # self.permission = Permission()
        # self.query = None

    def signin(self):
        self.auth_controller.login()
        if self.auth_controller.user_instance is not None:
            return self.start(user=self.auth_controller.user_instance)
        else:
            return self.signin()

    def start(self, user):
        view.menu_name(self.name)
        view.dict_k(self.actions_by_role[user.id])
        choice = view.user_input()

        if choice == "logout":
            self.auth_controller.logout()
            self.signin()
        elif choice in self.actions_by_role[user.id].keys():
            view.dict_kv_func(self.actions_by_role[user.id][choice])
            sub_choice = int(view.user_input())
            if sub_choice in self.actions_by_role[user.id][choice].keys():
                with self.session.begin() as session:
                    self.actions_by_role[user.id][choice][sub_choice](
                        session=session, user=user
                    )
                    return self.start(user=user)
            else:
                view.error_input()
                return self.start(user=user)
        else:
            view.error_input()
            return self.start(user=user)
