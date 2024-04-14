from werkzeug.security import check_password_hash
from ..models.user_model import User
from ..core.extensions import db
from ..core.utils import generate_access_token, generate_refresh_token, hash_token
from flask import current_app as app
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.errors import AuthErrorException
from ..models.token_block_list_model import RefreshToken


def check_password(user_password, current_password):
    """
    Verifies whether the provided password matches the hashed password.

    Args:
        user_password (str): The hashed password stored in the database.
        current_password (str): The plaintext password provided by the user.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    verification_res = check_password_hash(user_password, current_password)
    return verification_res


def login_process(email, password):
    """
    Handles the login process for a user. Verifies the email and password,
    generates access and refresh tokens, stores the refresh token in the database.

    Args:
        email (str): The email of the user trying to log in.
        password (str): The plaintext password provided by the user.

    Returns:
        tuple: A tuple containing the generated access token and refresh token.
            - access_token (str): The JWT access token.
            - refresh_token (str): The JWT refresh token.

    Raises:
        AuthErrorException: If the email does not exist or the password is incorrect.
        IntegrityErrorException: If there is an integrity issue with the database (e.g., unique constraint violation).
        DataErrorException: If the data provided is invalid or too large for the database.
        OperationalErrorException: If there is a database connection issue.
    """
    try:
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
                                            expiration_minutes=app.config.get("JWT_ACCESS_TOKEN_EXP_MIN"))
        
        refresh_token = generate_refresh_token(user.id, 
                                            user.email, 
                                            app.config.get("JWT_REFRESH_SECRET_KEY"), 
                                            expiration_day=app.config.get("JWT_REFRESH_TOKEN_EXP_DAY"))
        
        app.logger.info("Generated Access Token and Refresh Token: %s", email)
        
        # storing refresh token in db 
        token_entry = RefreshToken(
            user_id = user.id,
            token_hash = hash_token(refresh_token),
        )
        
        db.session.add(token_entry)
        db.session.commit()

        return access_token, refresh_token
    
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning("Invalid constraints for email: %s", email)
        raise IntegrityErrorException("Invalid constraints") from e

    except DataError as e:
        db.session.rollback()
        app.logger.warning("Provided data is invalid or too large for email: %s", email)
        raise DataErrorException("Provided data is invalid or too large.") from e
    
    except OperationalError as e:
        db.session.rollback()
        app.logger.warning("Database connection problem for email: %s", email)
        raise OperationalErrorException("Database connection problem. Please try again later.") from e
