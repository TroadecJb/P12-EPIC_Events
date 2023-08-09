import bcrypt


def pwd_hashed(pwd):
    """testance"""
    hash = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hash
