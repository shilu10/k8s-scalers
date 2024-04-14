import jwt 
import datetime 
from flask import current_app as app
import uuid
import hashlib
from .errors import ExpiredTokenError, InvalidTokenError


def generate_access_token(user_id, user_email, secret_key, expiration_minutes):
    """
    Generates an access token for the user with a specified expiration time.

    Args:
        user_id (str or int): The unique identifier of the user.
        user_email (str): The email address of the user.
        secret_key (str): The secret key used to sign the token.
        expiration_minutes (int): The expiration time of the token in minutes.

    Returns:
        str: The generated JWT access token.
    
    Raises:
        Exception: If the token cannot be generated due to an unexpected error.
    """
    jti = str(uuid.uuid4())  # Unique JWT ID
    payload = {
        'sub': str(user_id),  # Subject (user ID)
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=expiration_minutes),  # Expiration time
        'iat': datetime.datetime.now(),  # Issued at time
        'email': user_email  # User email
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')  # Encoding the token
    return token


def decode_jwt_token(token, secret_key):
    """
    Decodes and verifies the given JWT token using the provided secret key.

    Args:
        token (str): The JWT token to decode.
        secret_key (str): The secret key to verify the token.

    Returns:
        dict: The decoded JWT payload if the token is valid.

    Raises:
        InvalidTokenError: If the token is invalid.
        ExpiredTokenError: If the token has expired.
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    
    except jwt.ExpiredSignatureError:
        # Raise a custom exception for expired tokens
        raise ExpiredTokenError('Token has expired')
    
    except jwt.InvalidTokenError:
        # Raise a custom exception for invalid tokens
        raise InvalidTokenError('Invalid Token')


def generate_refresh_token(user_id, user_email, secret_key, expiration_day):
    """
    Generates a refresh token for the user with a specified expiration period.

    Args:
        user_id (str or int): The unique identifier of the user.
        user_email (str): The email address of the user.
        secret_key (str): The secret key used to sign the token.
        expiration_day (int): The expiration time of the refresh token in days.

    Returns:
        str: The generated JWT refresh token.
    
    Raises:
        Exception: If the token cannot be generated due to an unexpected error.
    """
    payload = {
        'sub': str(user_id),  # Subject (user ID)
        'iat': datetime.datetime.now(),  # Issued at time
        'exp': datetime.datetime.now() + datetime.timedelta(days=expiration_day),  # Expiration time
        'email': user_email  # User email
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")  # Encoding the refresh token
    return token


def hash_token(token: str) -> str:
    """
    Hashes the given token using SHA-256 algorithm.

    Args:
        token (str): The token string to hash.

    Returns:
        str: The hashed token as a hexadecimal string.
    """
    return hashlib.sha256(token.encode()).hexdigest()
