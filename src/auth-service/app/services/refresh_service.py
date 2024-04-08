from flask import current_app as app 
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.extensions import db
from ..models.token_block_list_model import RefreshToken
from ..core.utils import decode_jwt_token, generate_access_token, generate_refresh_token, hash_token
from ..core.errors import TokenErrorException, DataErrorException, IntegrityErrorException, OperationalErrorException


def refresh_process(old_refresh_token):
    try:
        payload = decode_jwt_token(old_refresh_token, app.config.get("JWT_REFRESH_SECRET_KEY"))

        user_id = payload["sub"]
        email = payload["email"]
        app.logger.info("Refresh attempt with email: %s", email)

        hashed_refresh_token = hash_token(old_refresh_token)
        token_entry = db.session.query(RefreshToken).filter_by(user_id=user_id, token_hash=hashed_refresh_token).first()

        if not token_entry or token_entry.revoked:
            app.logger.warning("old token is invalid for email: %s", email)
            raise TokenErrorException("Invalid Token")
        
        # revoking the old refresh token
        token_entry.revoked  = True
        db.session.commit()
        app.logger.info("Old Token entry is revoked for email: %s", email)

        # Generate new access token (valid for 15 minutes)
        access_token = generate_access_token(user_id, email, app.config.get("JWT_ACCESS_SECRET_KEY"), 1)
        new_refresh_token = generate_refresh_token(user_id, email, app.config.get("JWT_REFRESH_SECRET_KEY"), 7)
        app.logger.info("Generated new access token and refresh token for email: %s", email)

        new_token_entry = RefreshToken(
                            user_id = user_id,
                            token_hash = hash_token(new_refresh_token)
                        )
        db.session.add(new_token_entry)
        db.session.commit()
        app.logger.info("New Token entry is added for email: %s", email)

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
    
