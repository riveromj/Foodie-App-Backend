import jwt
import datetime

#+ datetime.timedelta(minutes=) --> Esto es para añadir un tiempo despues del cual caduca el token
def encode_token(user, key):
    return jwt.encode({"user":user, "exp":datetime.datetime.utcnow() }, key)

def decode_token(token, key):
    return jwt.decode(token, key, algorithms="HS256")