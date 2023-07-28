import bcrypt


def signup():
    email = input("Enter email address: ")
    pwd = input("Enter password: ").encode()
    conf_pwd = input("Confirm password: ").encode()

    # check if bcrypt directly on the input is more secure
    if conf_pwd == pwd:
        secure_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
    else:
        print("Passwords don't match!")

    # directly record in db or send to another function to do so
    return email, secure_pwd


def login():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")

    secure_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())

    # directly check in db or send to another function
    return email, secure_pwd
