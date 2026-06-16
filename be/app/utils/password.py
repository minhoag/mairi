import bcrypt


# Hash a password for the first time
def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))


# Check hashed password. Using bcrypt, the salt is saved into the hash itself
def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)
