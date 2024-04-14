from flask import render_template, jsonify, request, Blueprint, abort, current_app as app
from ..schema.login_schema import LoginSchema
from ..services.login_service import login_process
from ..core.errors import (
    AuthErrorException, 
    DataErrorException, 
    OperationalErrorException, 
    IntegrityErrorException
)
from ..core.response_builder import success_response, error_response
from ..core.extensions import db
from marshmallow import ValidationError


login_bp = Blueprint("login_bp", __name__)
login_schema = LoginSchema()

@login_bp.route("/login", methods=["POST"])
def login():
    """
    Handles user login.

    Expects:
        JSON payload with 'email' and 'password'.

    Returns:
        - 200: On successful login with access and refresh tokens.
        - 400: On validation or authentication errors.
        - 500: On internal errors like DB integrity or operational errors.
    """
    login_data = request.get_json()

    if not login_data:
        app.logger.warning("No login data received in request")
        return error_response("No input data provided", 400)

    email = login_data.get("email")
    app.logger.info("Login attempt received for email: %s", email)

    try:
        validated_data = login_schema.load(login_data)

    except ValidationError as err:
        app.logger.warning("Login validation error for email %s: %s", email, err.messages)
        return error_response(err.messages, 400)
    
    except Exception as err:
        app.logger.error("Unexpected error during login schema validation for email %s: %s", email, str(err))
        return error_response("Invalid input format", 400)

    try:
        access_token, refresh_token = login_process(validated_data["email"], validated_data["password"])
        app.logger.info("Login successful for email: %s, access token issued.", email)

        return success_response(data={
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    except AuthErrorException as err:
        app.logger.warning("Authentication failed for email: %s: %s", email, str(err))
        return error_response(str(err), 400)

    except (IntegrityErrorException, DataErrorException, OperationalErrorException) as err:
        app.logger.error("Internal login error for email %s: %s", email, type(err).__name__)
        return error_response("Internal server error", 500)
    except Exception as err:
        app.logger.exception("Unexpected error in login service for email %s: %s", email, str(err))
        return error_response("Internal server error", 500)
