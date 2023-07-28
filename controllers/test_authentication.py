import bcrypt

from models.users import User

y = User()
print(y, type(y))

from views.menu import vauthentication


def hash_salt_password(user_pw):
    return bcrypt.hashpw(user_pw, bcrypt.gensalt())


def check_password(user_pw, hashed_pw):
    if bcrypt.checkpw(user_pw, hashed_pw):
        pass
    else:
        pass


x = vauthentication()
print(x)
