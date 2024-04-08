from flask import jsonify, request, Blueprint
from ..schema.signup_schema import SignUpSchema
from ..services.signup_service import signup_process
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException
from ..core.response_builder import success_response, error_response
from flask import current_app as app


signup_bp = Blueprint("signup_bp", __name__)
signup_schema = SignUpSchema()


@signup_bp.route("/api/auth/v1/signup", methods=["POST"])
def signup():
    req_data = request.get_json()
    app.logger.info("Signup attempt with email: %s", req_data.get("email"))

    # Validate schema
    try:
        schema_res = signup_schema.load(req_data)

    except Exception as err:
        app.logger.warning("Signup schema validation failed: %s", str(err))
        return error_response(str(err), 400)

    email = schema_res["email"]
    password = schema_res["password"]

    # Call signup process
    try:
        signup_process_response = signup_process(email, password)
        app.logger.info("Signup successful for email: %s", email)
        return success_response(signup_process_response.get("message"), 200)
    
    except IntegrityErrorException as e:
        app.logger.warning("Signup attempt failed due to IntegrityError with email: %s", email)
        return error_response(str(e), 400)
    
    except DataErrorException as e:
        app.logger.warning("Signup attempt failed due to DataError with email: %s", email)
        return error_response(str(e), 400)
    
    except OperationalErrorException as e:
        app.logger.error("Signup attempt failed due to OperationalError with email: %s", email)
        return error_response(str(e), 500)
    
    except Exception as e:
        app.logger.error("Signup attempt failed with unknown error: %s", str(e))
        return error_response(str(e), 500)