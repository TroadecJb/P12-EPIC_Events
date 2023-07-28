def vauthentication():
    print("\n- - - Authentication ---")
    user_email = input("Enter email address : ")
    user_mdp = input("Enter password : ").encode()

    return user_email, user_mdp
