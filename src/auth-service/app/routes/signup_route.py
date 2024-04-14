from flask import Blueprint, request, current_app as app
from ..schema.signup_schema import SignUpSchema
from ..services.signup_service import signup_process
from ..core.errors import (
    IntegrityErrorException,
    DataErrorException,
    OperationalErrorException,
    ValidationErrorException
)
from ..core.response_builder import success_response, error_response
from marshmallow import ValidationError


signup_bp = Blueprint("signup_bp", __name__)
signup_schema = SignUpSchema()


@signup_bp.route("/signup", methods=["POST"])
def signup():
    """
    User signup endpoint.

    Accepts: JSON payload with 'email' and 'password'.
    Returns:
        - 200: On success
        - 400: On bad input or known validation issues
        - 500: On server/database failures
    """
    req_data = request.get_json(silent=True)

    if not req_data or "email" not in req_data or "password" not in req_data:
        app.logger.warning("Signup failed: missing 'email' or 'password' in request.")
        return error_response("Missing required fields: email or password", 400)

    email = req_data.get("email")
    app.logger.info("Signup attempt with email: %s", email[:10] + '...')  # Mask email for logging

    # Schema validation
    try:
        schema_res = signup_schema.load(req_data)
        email = schema_res["email"]
        password = schema_res["password"]

    except ValidationError as err:
        app.logger.warning("Signup schema validation failed for email %s: %s", email, err.messages)
        return error_response("Invalid signup data", 400)
    
    except Exception as err:
        app.logger.warning("Unexpected error during schema validation for email %s: %s", email, str(err))
        return error_response("Invalid signup data", 400)

    # Service logic
    try:
        signup_process_response = signup_process(email, password)
        app.logger.info("Signup successful for email: %s", email[:10] + '...')  # Mask email for logging
        return success_response(signup_process_response.get("message"), 200)

    except IntegrityErrorException as e:
        app.logger.warning("Signup failed due to integrity error for email: %s", email[:10] + '...')
        return error_response("Email already exists or data constraint violated", 400)

    except DataErrorException as e:
        app.logger.warning("Signup failed due to data error for email: %s", email[:10] + '...')
        return error_response("Invalid data provided", 400)

    except OperationalErrorException as e:
        app.logger.error("Signup failed due to operational error for email: %s", email[:10] + '...')
        return error_response("Internal server error", 500)

    except ValidationErrorException as e:
        app.logger.error("Signup failed due to validation logic error for email: %s", email[:10] + '...')
        return error_response("Validation failed", 400)

    except Exception as e:
        app.logger.exception("Signup failed due to unexpected error for email: %s", email[:10] + '...')
        return error_response("Unexpected error occurred", 500)
