from flask import Blueprint, jsonify, request
from ..core.response_builder import success_response, error_response
from flask import current_app as app
from ..core.utils import decode_jwt_token
from ..core.extensions import db 
from ..models.jwt_revocation_model import RevokedToken
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException


logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/api/auth/v1/logout", methods=["POST"])
def logout_process():
    try:
        request_data = request.get_json()

        if not request_data or not request_data.get("refresh_token"):
            app.logger.warning("No Refresh Token provided in request body for logout")
            return error_response("No Refresh Token provided", 400)

        refresh_token = request_data.get("refresh_token")
        payload = decode_jwt_token(refresh_token, app.config.get("JWT_REFRESH_SECRET_KEY"))

        expiration_time = payload.get("exp")
        email = payload.get("email")  # Get email from decoded token for logging

        app.logger.info("Logout Initiated for %s..", email)

        # Store revoked token in the DB
        revoked_token = RevokedToken(
                            refresh_token=refresh_token,
                            expiration_time=expiration_time
                        )

        db.session.add(revoked_token)
        db.session.commit()

        app.logger.info("Token revoked successfully for email: %s", email)

        return success_response({
            "message": "Logout successful, token has been revoked."
        })

    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning("Token already exists or invalid constraints for email: %s", email)
        raise IntegrityErrorException("Email already exists or invalid constraints") from e

    except DataError as e:
        db.session.rollback()
        app.logger.warning("Provided data is invalid or too large for email: %s", email)
        raise DataErrorException("Provided data is invalid or too large.") from e

    except OperationalError as e:
        db.session.rollback()
        app.logger.warning("Database connection problem for email: %s", email)
        raise OperationalErrorException("Database connection problem. Please try again later.") from e

    except Exception as err:
        app.logger.error("Logout failed: %s", str(err))
        return error_response(str(err), 400)
