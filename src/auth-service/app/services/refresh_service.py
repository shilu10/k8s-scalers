from flask import current_app as app 
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.extensions import db
from ..models.token_block_list_model import RefreshToken
from ..core.utils import decode_jwt_token, generate_access_token, generate_refresh_token, hash_token
from ..core.errors import TokenErrorException, DataErrorException, IntegrityErrorException, OperationalErrorException


def refresh_process(old_refresh_token):
    """
    Handles the process of refreshing the access and refresh tokens. The old refresh token is validated, revoked,
    and a new access token and refresh token are generated for the user. The new refresh token is stored in the database.

    Args:
        old_refresh_token (str): The refresh token provided by the user to refresh the session.

    Returns:
        tuple: A tuple containing:
            - access_token (str): The newly generated access token (valid for a short period).
            - new_refresh_token (str): The newly generated refresh token (valid for a longer period).
            - email (str): The email of the user for confirmation.

    Raises:
        TokenErrorException: If the old refresh token is invalid, expired, or already revoked.
        IntegrityErrorException: If there is a violation of integrity constraints during the database operations.
        DataErrorException: If the data provided is invalid or too large for the database.
        OperationalErrorException: If there is a database connection issue or operational error.
    """
    try:
        # Decode the old refresh token
        payload = decode_jwt_token(old_refresh_token, app.config.get("JWT_REFRESH_SECRET_KEY"))

        user_id = payload["sub"]
        email = payload["email"]
        app.logger.info("Refresh attempt with email: %s", email)

        # Hash the refresh token for lookup
        hashed_refresh_token = hash_token(old_refresh_token)
        token_entry = db.session.query(RefreshToken).filter_by(user_id=user_id, token_hash=hashed_refresh_token).first()

        if not token_entry or token_entry.revoked:
            app.logger.warning("Old token is invalid for email: %s", email)
            raise TokenErrorException("Invalid Token")
        
        # Revoke the old refresh token
        token_entry.revoked = True
        db.session.commit()
        app.logger.info("Old token entry is revoked for email: %s", email)

        # Generate new access and refresh tokens
        access_token = generate_access_token(user_id, email, app.config.get("JWT_ACCESS_SECRET_KEY"), 1)
        new_refresh_token = generate_refresh_token(user_id, email, app.config.get("JWT_REFRESH_SECRET_KEY"), 7)
        app.logger.info("Generated new access token and refresh token for email: %s", email)

        # Store the new refresh token in the database
        new_token_entry = RefreshToken(
                            user_id=user_id,
                            token_hash=hash_token(new_refresh_token)
                        )
        db.session.add(new_token_entry)
        db.session.commit()
        app.logger.info("New token entry is added for email: %s", email)

        return access_token, new_refresh_token, email
    
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
