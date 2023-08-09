from utils.basic_utils import pwd_hashed


class Menu:
    def sign_in(self):
        print("\n- - - Sign-in - - -")
        email = input("Enter email address : ")
        pwd = input("Enter password : ").encode("utf-8")
        conf_pwd = input("Confirm password : ").encode("utf-8")

        if pwd != conf_pwd:
            print("\n\tOops passwords don't match, please retry.")
            self.sign_in()
        else:
            pwd = pwd_hashed(pwd)

            return (email, pwd)

    def log_in(self):
        print("\n- - - Log-in - - -")
        email = input("Enter email address : ")
        pwd = input("Enter password : ").encode("utf-8")

        return email, pwd

    def action_choice(self):
        print("\n- - -  Select action - - -")
        print("1-\tClients")
        print("2-\tContracts")
        print("3-\tCompanies")
        print("4-\tEvents")
        print("5-\tAddresses")
        print("6-\tUsers")
        choice = input("-> ")

        return choice
