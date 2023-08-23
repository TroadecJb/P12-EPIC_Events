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


class View:
    def user_input(self, detail="") -> str:
        choice = input(f"{fg.GREEN}{detail}-->{fg.RESET} ")
        if choice == "quit":
            print("quitting")
            quit()
        return choice.lower()

    def menu_name(self, name: str) -> str:
        print(f'\n{bg.CYAN}{name.center(40, " ")}{bg.RESET}')

    def submenu_name(self, name: str) -> str:
        print(f'\n{" {name} ".center(40, "-")}')

    def basic(self, message: str) -> str:
        print(message)

    def basic_list(self, obj: list) -> str:
        for i in obj:
            print()
            print(i[0])

    def basic_list_index(self, obj: list) -> str:
        """Enumerate list with int index"""
        for idx, i in enumerate(obj):
            print(f"{fg.YELLOW}{idx+1}{fg.RESET} {i}")

    def error_input(self) -> str:
        print("\nInvalid input\n")

    def error_message(self, message: str) -> str:
        print(f"\n{fg.RED}Something went wrong:{fg.RESET} {message}\n")

    def dict_k(self, dictionnary: dict) -> str:
        """Print dict's keys"""
        for k in dictionnary.keys():
            print("\t", fg.YELLOW, k, fg.RESET)

    def dict_kv_func(self, dictionnary: dict) -> str:
        """
        Print dict's key, value.
        "_" in value are replace by " ".
        """
        for k, v in dictionnary.items():
            print("\t", fg.YELLOW, k, fg.RESET, v.__name__.replace("_", " "))

    def log_in(self) -> tuple[str, bytes]:
        """Return email and password provided by user"""
        print(f'\n{bg.CYAN}{" Log-in ".center(40, " ")}{bg.RESET}')
        email = input(f"{fg.BLUE}email : {fg.RESET}")
        pwd = input(f"{fg.BLUE}password : {fg.RESET}").encode("utf-8")

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
