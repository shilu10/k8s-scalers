from flask import jsonify, request, Blueprint
from ..core.response_builder import success_response, error_response
from flask import current_app as app
from ..services.refresh_service import refresh_process
from ..core.errors import DataErrorException, OperationalErrorException, IntegrityErrorException


refresh_bp = Blueprint("refresh_bp", __name__)

@refresh_bp.route("/refresh", methods=["POST"])
def refresh():
    try:
        request_data = request.get_json()
        authorization_header = request.headers.get('Authorization', None)

        refresh_token = None

        # Priority: Authorization header -> body
        if authorization_header:
            if authorization_header.startswith("Bearer "):
                refresh_token = authorization_header.split(" ")[1]
            else:
                refresh_token = authorization_header

        elif request_data and request_data.get("refresh_token"):
            refresh_token = request_data.get("refresh_token")

        if not refresh_token:
            return error_response("No Refresh Token found", 400)

        access_token, new_refresh_token, email = refresh_process(old_refresh_token=refresh_token)

        return success_response({"access_token": access_token, "refresh_token": new_refresh_token})
    
    except IntegrityErrorException as err:
        app.logger.info("Login Process failed due to Integrity error for email: %s", email)
        return error_response(str(err), 500)
    
    except DataErrorException as err:
        app.logger.info("Login Process failed due to data error for email: %s", email)
        return error_response(str(err), 500)
    
    except OperationalErrorException as err:
        app.logger.info("Login Process failed due to operational error for email: %s", email)
        return error_response(str(err), 500)
    
    except Exception as err:
        # In error, don't assume payload exists
        app.logger.warning("Refresh attempt failed. Reason: %s", str(err))
        return error_response(str(err), 400)
