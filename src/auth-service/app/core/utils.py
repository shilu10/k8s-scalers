import jwt 
import datetime 
from flask import current_app as app
import uuid
import hashlib


def generate_access_token(user_id, user_email, secret_key, expiration_minutes):
    jti = str(uuid.uuid4())
    payload = {
        'sub': str(user_id), 
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=expiration_minutes),  # expires in 30 minutes
        'iat': datetime.datetime.now(),  # issued at
        'email': user_email  # subject (user data)
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_jwt_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    
    except jwt.ExpiredSignatureError as err:
        raise Exception('Token expired')
    
    except jwt.InvalidTokenError as err:
        raise Exception('Invalid Token')


def generate_refresh_token(user_id, user_email, secret_key, expiration_day):
    payload = {
        'sub': str(user_id),
        'iat': datetime.datetime.now(),
        'exp': datetime.datetime.now() + datetime.timedelta(days=expiration_day),
        'email': user_email  # subject (user data)
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
