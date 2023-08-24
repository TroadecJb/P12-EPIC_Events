from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PasswordValidator
import bcrypt
from views.color import fg, bg, style


class View:
    def user_input(self, detail="") -> str:
        """
        Return the input.
        If the input is 'quit', quit the script.

        Args:
            detail (str) : string to add contextual inforamtion (default is empty)

        Return:
            choice (str) : lower string
            quit(
        """
        choice = inquirer.text(message=detail).execute().lower()
        if choice == "quit":
            print("quitting")
            quit()
        return choice

    def menu_name(self, name: str) -> str:
        """
        Print the name centered (40 char lenght) with CYAN background

        Args:
            name (str) : Name of the menu

        Return:
            print
        """
        print(f'\n{bg.CYAN}{name.center(40, " ")}{bg.RESET}')

    def basic(self, message: str) -> str:
        """
        Print message

        Args:
            message (str) : message for contextual informations
        Return:
            print
        """
        print(message)

    def basic_list(self, obj: list):
        """
        Print each element of a list, spaced with a blank line

        Args:
            obj (list) : list of objects to iterate
        Return:
            Print

        """
        for i in obj:
            print()
            print(i)

    def error_input(self) -> str:
        """
        Print message "invalid input"

        Return:
            print
        """
        print("\nInvalid input\n")

    def error_message(self, message: str) -> str:
        """
        Print error message with custom contextual informations

        Args:
            message (str): contextual informations
        Return:
            print
        """
        print(f"\n{fg.RED}Something went wrong:{fg.RESET} {message}\n")

    def log_in(self) -> tuple[str, bytes]:
        """
        Return email and password provided by user input

        Args:
            none
        Returns:
            tuple (str, bytes) : email, password encoded in utf-8

        """
        email = inquirer.text(message="email :").execute()
        password = (
            inquirer.secret(
                message="password :",
                transformer=lambda _: "[hidden]",
            )
            .execute()
            .encode("utf-8")
        )
        return email, password

    def change_password(self, original_password) -> bytes:
        """
        Return new password after valdiation of the old one
        Args:
            original_password (bytes) : hashed & salted password
        Returns:
            new_password (bytes) : password encoded in utf-8
        """
        old_password = (
            inquirer.secret(
                message="current password :",
                transformer=lambda _: "[hidden]",
            )
            .execute()
            .encode("utf-8")
        )

        if bcrypt.checkpw(old_password, original_password):
            new_password = (
                inquirer.secret(
                    message="new password :",
                    validate=PasswordValidator(
                        length=8, cap=True, special=True, number=True
                    ),
                    transformer=lambda _: "[hidden]",
                    long_instruction="Password require length of 8, 1 cap char, 1 special char and 1 number char.",
                )
                .execute()
                .encode("utf-8")
            )
            return new_password
        else:
            return self.change_password(self, original_password)

    def select_obj_from_list(self, objs):
        """
        Enemurate list with int index.

        Args:
            objs (list) : List of objects to iterate through
        Return:
            choice (any) : object selected
        """
        choice = inquirer.select(
            message="select element :", choices=[Choice(obj) for obj in objs]
        ).execute()
        return choice

    def confirm(self, message=None):
        """
        Ask for the user to confirm, with contextual message (Default None)

        Args:
            message (any) : contextual information if neeeded
        Return:
            proceed (bool)
        """
        proceed = inquirer.confirm(message=message, default=True).execute()
        return proceed

    def select_action(self, message=None, action_dict=None):
        """
        Return the value selected by the user from a {key; value}.
        The key is used as a placeholder, humand readable.

        Args:
            message (str) : contextual information if needed
            action_dict (dict) : dictionnary with key as name and value as function
        Return:
            action (value) : value for the selected key

        """
        action = inquirer.select(
            message=message,
            choices=[Choice(v, name=k) for k, v in action_dict.items()],
        ).execute()
        return action

    def select_table_and_action(self, action_dict=None):
        """
        Return the value selected by the user from a {key; value}.
        The key is used as a placeholder, humand readable.
        With two forced choices: "logout" and "quit"

        Args:
            message (str) : contextual information if needed
            action_dict (dict) : dictionnary with key as name and value as function
        Return:
            action (value) : value for the selected key (or "logout" / "quit")

        """
        action = inquirer.select(
            message="Select table",
            choices=[Choice(v, name=k) for k, v in action_dict.items()],
        ).execute()
        if action == "logout":
            return "logout"
        elif action == "quit":
            return "quit"
        else:
            sub_action = inquirer.select(
                message="Select action",
                choices=[Choice(v, name=k) for k, v in action.items()],
            ).execute()
            if sub_action == "back":
                return "back"
            return sub_action
