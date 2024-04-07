from werkzeug.security import check_password_hash
from ..models.user_model import User
from ..core.extensions import db
from ..core.utils import generate_access_token, generate_refresh_token, decode_jwt_token
from flask import current_app as app
from ..core.errors import AuthErrorException


def check_password(user_password, current_password):
    verification_res = check_password_hash(user_password, current_password)

    return verification_res


def login_process(email, password):
    # Query user by email
    user = db.session.query(User).filter_by(email=email).first()

    # If user doesn't exist or password is wrong
    if user is None or not check_password(user.password, password):
        app.logger.warning("Invalid email or password: %s", email)
        raise AuthErrorException("Invalid email or password")  # 🔥 Generic message

    # If everything is correct
    access_token = generate_access_token(user.id, 
                                         user.email, 
                                         app.config.get("JWT_ACCESS_SECRET_KEY"), 
                                         expiration_minutes=1)
    
    refresh_token = generate_refresh_token(user.id, 
                                           user.email, 
                                           app.config.get("JWT_REFRESH_SECRET_KEY"), 
                                           expiration_day=7)
    app.logger.info("Generating Access Token and Refresh Token: %s", email)
    
    return access_token, refresh_token
