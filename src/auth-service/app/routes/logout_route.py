from flask import Blueprint, jsonify, request, current_app as app
from ..core.response_builder import success_response, error_response
from ..core.errors import SQLAlchemyErrorException, TokenErrorException
from ..services.logout_service import logout_process


logout_bp = Blueprint("logout_bp", __name__)


@logout_bp.route("/logout", methods=["POST"])
def logout():
    """
    Handles user logout by invalidating the provided refresh token.

    Expects:
        JSON payload with a 'refresh_token' field.

    Returns:
        - 200: If logout is successful.
        - 400: If the token is missing or invalid.
        - 500: For internal server/database errors.
    """
    try:
        request_data = request.get_json()

        if not request_data or not request_data.get("refresh_token"):
            app.logger.warning("Logout request missing 'refresh_token'. Request data: %s", request_data)
            return error_response("Refresh token is required", 400)

        refresh_token = request_data["refresh_token"]
        result = logout_process(refresh_token)

        # Truncating refresh token for security reasons
        app.logger.info("Logout successful for refresh token: %s", refresh_token[:10] + '...')
        return success_response(result.get("message"), 200)

    except TokenErrorException as err:
        app.logger.warning("Invalid refresh token during logout: %s", str(err))
        return error_response(str(err), 400)

    except SQLAlchemyErrorException as err:
        app.logger.error("Database error during logout: %s", str(err))
        return error_response("Internal server error", 500)

    except Exception as err:
        # Add more context if necessary (e.g., request details, user-agent)
        app.logger.exception("Unexpected error during logout. Request data: %s", request_data)
        return error_response("An unexpected error occurred", 500)
