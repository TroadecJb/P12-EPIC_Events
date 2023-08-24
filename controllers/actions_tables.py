from views.display import View

from controllers.authentication import Authentication_controller

from controllers import (
    actions_clients,
    actions_contracts,
    actions_events,
    actions_users,
)

view = View()


class ActionsManager:
    actions_admin = {
        "clients": {
            "read clients": actions_clients.read_clients,
            "add new client": actions_clients.create_client,
            "modify client info": actions_clients.update_client,
            "delete client": actions_clients.delete_client,
            "-BACK-": "back",
        },
        "contracts": {
            "read contracts": actions_contracts.read_contract,
            "add new contract": actions_contracts.create_contract,
            "modify contract": actions_contracts.update_contract,
            "delete contract": actions_contracts.delete_contract,
            "-BACK-": "back",
        },
        "events": {
            "read events": actions_events.read_event,
            "add new event": actions_events.create_event,
            "modify event": actions_events.update_event,
            "delete event": actions_events.delete_event,
            "-BACK-": "back",
        },
        "users": {
            "read users": actions_users.read_user,
            "add new user": actions_users.create_user,
            "modify user": actions_users.update_user,
            "delete user": actions_users.delete_user,
            "modify password": actions_users.change_password,
            "-BACK-": "back",
        },
        "-LOGOUT-": "logout",
        "-CLOSE-": "quit",
    }
    actions_manager = {
        "clients": {"read clients": actions_clients.read_clients, "-BACK-": "back"},
        "contracts": {
            "read contracts": actions_contracts.read_contract,
            "add new contract": actions_contracts.create_contract,
            "modify contract": actions_contracts.update_contract,
            "-BACK-": "back",
        },
        "events": {
            "read events": actions_events.read_event,
            "modify event": actions_events.update_event,
            "-BACK-": "back",
        },
        "users": {
            "read users": actions_users.read_user,
            "add new user": actions_users.create_user,
            "modify user": actions_users.update_user,
            "delete user": actions_users.delete_user,
            "modify password": actions_users.change_password,
            "-BACK-": "back",
        },
        "-LOGOUT-": "logout",
        "-CLOSE-": "quit",
    }
    actions_sale = {
        "clients": {
            "read clients": actions_clients.read_clients,
            "add new client": actions_clients.create_client,
            "modify client": actions_clients.update_client_in_charge,
            "-BACK-": "back",
        },
        "contracts": {
            "read contracts": actions_contracts.read_contract,
            "modify contract": actions_contracts.update_contract,
            "-BACK-": "back",
        },
        "events": {
            "read events": actions_events.read_event,
            "add new event": actions_events.create_event,
            "-BACK-": "back",
        },
        "users": {"modify password": actions_users.change_password, "-BACK-": "back"},
        "-LOGOUT-": "logout",
        "-CLOSE-": "quit",
    }
    action_support = {
        "clients": {
            "read clients": actions_clients.read_clients,
            "-BACK-": "back",
        },
        "contracts": {
            "read contracts": actions_contracts.read_contract,
            "-BACK-": "back",
        },
        "events": {
            "read events": actions_events.read_event,
            "read eents in charge": actions_events.read_event_in_charge,
            "modify event": actions_events.update_event_in_charge,
            "-BACK-": "back",
        },
        "users": {
            "modify password": actions_users.change_password,
            "-BACK-": "back",
        },
        "-LOGOUT-": "logout",
        "-CLOSE-": "quit",
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
        self.user = None
        self.user_actions = None

    def signin(self):
        self.auth_controller.login()
        if self.auth_controller.user_instance is not None:
            self.user = self.auth_controller.user_instance
            self.user_actions = self.actions_by_role[self.user.id]
            return self.start(user=self.user)

        else:
            return self.signin()

    def start(self, user):
        view.menu_name(self.name)
        action = view.select_table_and_action(action_dict=self.user_actions)
        if action == "logout":
            self.auth_controller.logout()
            self.user = None
            return self.signin()
        elif action == "quit":
            return quit()
        elif action == "back":
            return self.start(user=user)
        else:
            with self.session.begin() as session:
                action(session=session, user=user)

        return self.start(user=user)
