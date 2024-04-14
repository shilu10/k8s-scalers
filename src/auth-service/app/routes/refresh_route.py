from flask import Blueprint, jsonify, request, current_app as app
from ..core.response_builder import success_response, error_response
from ..services.refresh_service import refresh_process
from ..core.errors import DataErrorException, OperationalErrorException, IntegrityErrorException


refresh_bp = Blueprint("refresh_bp", __name__)


@refresh_bp.route("/refresh", methods=["POST"])
def refresh():
    """
    Issues a new access and refresh token using a valid old refresh token.

    Token priority:
        1. Authorization header (Bearer token)
        2. 'refresh_token' field in JSON body

    Returns:
        - 200: New tokens if successful
        - 400: If token is missing or invalid
        - 500: On internal server/database errors
    """
    try:
        request_data = request.get_json(silent=True) or {}
        authorization_header = request.headers.get("Authorization")

        refresh_token = None

        # Extract refresh token from Authorization header or request body
        if authorization_header:
            if authorization_header.startswith("Bearer "):
                refresh_token = authorization_header.split(" ")[1]
            else:
                refresh_token = authorization_header
        elif request_data.get("refresh_token"):
            refresh_token = request_data["refresh_token"]

        if not refresh_token:
            app.logger.warning("No refresh token provided in header or body")
            return error_response("No refresh token provided", 400)

        # Process token refresh
        access_token, new_refresh_token, email = refresh_process(old_refresh_token=refresh_token)

        # Log success but mask the refresh token
        app.logger.info("Token refresh successful for email: %s", email)

        # Only return the new tokens in the response
        return success_response({
            "access_token": access_token,
            "refresh_token": new_refresh_token
        })

    except IntegrityErrorException as err:
        app.logger.error("Integrity error during token refresh for refresh_token (masked): %s", refresh_token[:10] + '...')
        return error_response("Database integrity issue", 500)

    except DataErrorException as err:
        app.logger.error("Data error during token refresh for refresh_token (masked): %s", refresh_token[:10] + '...')
        return error_response("Invalid data", 500)

    except OperationalErrorException as err:
        app.logger.error("Operational error during token refresh for refresh_token (masked): %s", refresh_token[:10] + '...')
        return error_response("Operational database error", 500)

    except Exception as err:
        app.logger.exception("Unexpected error during token refresh for refresh_token (masked): %s", refresh_token[:10] + '...')
        return error_response("Token refresh failed", 400)
