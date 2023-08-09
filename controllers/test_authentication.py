import bcrypt


def hash_salt_password(user_pw):
    hashed = bcrypt.hashpw(user_pw, bcrypt.gensalt())
    return hashed


def check_password(user_pw, hashed_pw):
    if bcrypt.checkpw(user_pw, hashed_pw):
        print("yes")
    else:
        print("no")


pwd = input("password :").encode("utf-8")
x = hash_salt_password(pwd)

conf_pwd = input("conf pwd :").encode("utf-8")
y = hash_salt_password(conf_pwd)

print(check_password(conf_pwd, x))
