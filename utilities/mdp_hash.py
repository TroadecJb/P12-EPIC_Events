import bcrypt

# turn input's string into bytes
password = input("enter password : ").encode()


hashed = bcrypt.hashpw(password, bcrypt.gensalt())


if bcrypt.checkpw(password, hashed):
    print("2, it matches!")
else:
    print("Does not match :(")
