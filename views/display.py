class View:
    def user_input(self, detail="") -> str:
        choice = input(f"{detail}--> ")
        return choice

    def menu_name(self, name: str) -> str:
        print("\n", f" {name} ".center(40, "#"))

    def submenu_name(self, name: str) -> str:
        print("\n", f" {name} ".center(40, "-"))

    def basic(self, message: str) -> str:
        print(message)

    def basic_list(self, obj: list) -> str:
        for i in obj:
            print(i)

    def error_input(self) -> str:
        print("\nInvalid input\n")

    def error_message(self, message: str) -> str:
        print(f"\nSomething went wrong: {message}\n")

    def dict_kv_func(self, dictionnary: dict) -> str:
        for k, v in dictionnary.items():
            print("\t", k, v.__name__.replace("_", " "))

    def log_in(self) -> tuple[str, bytes]:
        """Return email and password provided by user"""
        print(" Log-in ".center(40, "#"))
        email = input("email : ")
        pwd = input("password : ").encode("utf-8")

        return email, pwd
