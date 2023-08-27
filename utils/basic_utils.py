import bcrypt


def pwd_hashed(pwd):
    hash = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hash
