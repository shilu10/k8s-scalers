from flask import current_app as app 
from sqlalchemy.exc import SQLAlchemyError
from ..core.extensions import db 
from ..models.token_block_list_model import RefreshToken
from ..core.utils import decode_jwt_token, hash_token
from ..core.errors import TokenErrorException, SQLAlchemyErrorException


def logout_process(refresh_token):
    """
    Handles the logout process by decoding the provided refresh token, checking its validity,
    and revoking the token in the database. If the token is valid and not revoked, it is marked as revoked.

    Args:
        refresh_token (str): The refresh token provided by the user to log out.

    Returns:
        dict: A dictionary containing a message confirming the logout, e.g., 
            {"message": "Logout successful"}

    Raises:
        TokenErrorException: If the token is invalid, already revoked, or there is any error related to token handling.
        SQLAlchemyErrorException: If a database-related error occurs while processing the token (e.g., query or commit failure).
        Exception: A generic exception handler to catch unexpected errors.
    """
    try:
        # Decode the token
        payload = decode_jwt_token(refresh_token, app.config.get("JWT_REFRESH_SECRET_KEY"))

        # Extract user ID and email
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id:
            raise TokenErrorException("Invalid token: no user ID found.")

        # Hash the refresh token for lookup
        hashed_refresh_token = hash_token(refresh_token)

        # Query the token from DB
        token_entry = db.session.query(RefreshToken).filter_by(
            user_id=user_id,
            token_hash=hashed_refresh_token
        ).first()

        if not token_entry or token_entry.revoked:
            raise TokenErrorException("Invalid or already revoked token.")

        # Revoke and commit
        token_entry.revoked = True
        db.session.commit()

        app.logger.info("Token revoked successfully for email: %s", email)

        return {
            "message": "Logout successful"
        }

    except TokenErrorException as te:
        app.logger.warning("Token error: %s", str(te))
        raise te  # Reraise for upper layer to handle as custom response

    except SQLAlchemyError as db_err:
        db.session.rollback()
        app.logger.error("Database error during logout: %s", str(db_err))
        raise SQLAlchemyErrorException("Internal server error during logout.")

    except Exception as e:
        app.logger.error("Unexpected error in logout_process: %s", str(e))
        raise TokenErrorException("Unexpected error occurred.")
