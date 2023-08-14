def user_input():
    choice = input("--> ")
    return choice


def show(message):
    print(message)


def show_error_input():
    print("\nInvalid input\n")


def show_error_message(message):
    print(f"\nSomething went wrong: {message}\n")


def show_dict_kv(dictionnary):
    for k, v in dictionnary.items():
        print("\t", k, v)


def log_in() -> tuple[str, bytes]:
    """Return email and password provided by user"""
    print("\n- - - Log-in - - -")
    email = input("Enter email address : ")
    pwd = input("Enter password : ").encode("utf-8")

    return email, pwd
