from models.roles import Commercial, Manager, Suppport
from models.users import User

# utilisateur = User()


def main():
    choix = input("1 commercial, 2 support, 3 manager : ")
    if choix == "1":
        utilisateur = User(Commercial())
        utilisateur.user_test()
        utilisateur.commercial_test()
    elif choix == "2":
        utilisateur = Suppport()
        utilisateur.user_test()
        utilisateur.support_test()
    elif choix == "3":
        utilisateur = Manager()
        utilisateur.user_test()
        utilisateur.manager_test()
    else:
        print("oups")


if __name__ == "__main__":
    main()
