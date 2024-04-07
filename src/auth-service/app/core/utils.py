import jwt 
import datetime 
import app 


def create_jwt_token(data, secret_key, expiration_minutes):
    payload = {
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=expiration_minutes),  # expires in 30 minutes
        'iat': datetime.datetime.now(),  # issued at
        'sub': data  # subject (user data)
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_jwt_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return {
            "success": True,
            "data": payload['sub']
        }  # return the user data
    
    except jwt.ExpiredSignatureError as err:
        raise Exception('Token expired')
    
    except jwt.InvalidTokenError as err:
        raise Exception('Invalid Token')
