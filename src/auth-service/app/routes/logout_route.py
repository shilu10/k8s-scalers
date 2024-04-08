from flask import Blueprint, jsonify, request
from ..core.response_builder import success_response, error_response
from flask import current_app as app
from ..core.errors import SQLAlchemyErrorException, TokenErrorException
from ..services.logout_service import logout_process


logout_bp = Blueprint("logout_bp", __name__)

@logout_bp.route("/logout", methods=["POST"])
def logout():
    try:
        request_data = request.get_json()

        if not request_data or not request_data.get("refresh_token"):
            app.logger.warning("No Refresh Token provided in request body for logout")
            return error_response("No Refresh Token provided", 400)

        refresh_token = request_data.get("refresh_token")
        logout_process_response = logout_process(refresh_token)

        return success_response(logout_process_response.get("message"), 200)

    except SQLAlchemyErrorException as err:
        app.logger.warning("Logout failed: %s", str(err))
        return error_response(str(err), 500)
    
    except TokenErrorException as err:
        app.logger.warning("Logout failed: %s", str(err))
        return error_response(str(err), 400)

    except Exception as err:
        app.logger.error("Logout failed: %s", str(err))
        return error_response(str(err), 400)
