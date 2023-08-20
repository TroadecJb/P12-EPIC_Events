class View:
    def user_input(self, detail="") -> str:
        choice = input(f"{detail}--> ")
        return choice.lower()

    def menu_name(self, name: str) -> str:
        print("\n", f" {name} ".center(40, "#"))

    def submenu_name(self, name: str) -> str:
        print("\n", f" {name} ".center(40, "-"))

    def basic(self, message: str) -> str:
        print(message)

    def basic_list(self, obj: list) -> str:
        for i in obj:
            print(i)

    def basic_list_index(self, obj: list) -> str:
        """Enumerate list with int index"""
        for idx, i in enumerate(obj):
            print(f"{idx+1} {i}")

    def error_input(self) -> str:
        print("\nInvalid input\n")

    def error_message(self, message: str) -> str:
        print(f"\nSomething went wrong: {message}\n")

    def dict_k(self, dictionnary: dict) -> str:
        """Print dict's keys"""
        for k in dictionnary.keys():
            print("\t", k)

    def dict_kv_func(self, dictionnary: dict) -> str:
        """
        Print dict's key, value.
        "_" in value are replace by " ".
        """
        for k, v in dictionnary.items():
            print("\t", k, v.__name__.replace("_", " "))

    def log_in(self) -> tuple[str, bytes]:
        """Return email and password provided by user"""
        print(" Log-in ".center(40, "#"))
        email = input("email : ")
        pwd = input("password : ").encode("utf-8")

        return email, pwd

    def select_from(self, list):
        """
        Enemurate list with int index.
        return obj from the list based on user input as index
        """
        self.basic_list_index(list)
        choice = int(self.user_input())
        if choice - 1 <= len(list):
            return list[choice - 1]
        else:
            self.error_input()
            return self.select_from(list)
