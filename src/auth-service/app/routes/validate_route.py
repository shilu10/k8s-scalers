from flask import Blueprint, request, current_app as app
from ..core.response_builder import success_response, error_response
from ..core.utils import decode_jwt_token  # Custom function for decoding JWT
from ..schema.validate_schema import ValidateSchema
from marshmallow import ValidationError

# Assuming these are the custom exceptions your `decode_jwt_token` might raise
from ..core.errors import InvalidTokenError, ExpiredTokenError, TokenError

validate_bp = Blueprint("validate_bp", __name__)
validate_schema = ValidateSchema()


@validate_bp.route("/validate-access-token", methods=["POST"])
def validate_token():
    """
    Validates the access token passed in the request body.

    Expected JSON:
        {
            "access_token": "<token>"
        }

    Returns:
        - 200: Token is valid
        - 400: Invalid token or schema
    """
    # Parse the JSON body
    try:
        request_data = request.get_json()
    except Exception as err:
        app.logger.warning("Failed to parse request JSON: %s", str(err))
        return error_response("Invalid JSON format", 400)

    if not request_data or "access_token" not in request_data:
        app.logger.warning("Access token missing from request body")
        return error_response("Access token is required", 400)

    access_token = request_data.get("access_token")

    # Schema validation
    try:
        validate_schema.load(request_data)
        app.logger.info("Validate schema validation successful")

    except ValidationError as err:
        app.logger.warning("Schema validation failed: %s", err.messages)
        return error_response("Invalid request payload", 400)
    
    except Exception as err:
        app.logger.warning("Unexpected error during schema validation: %s", str(err))
        return error_response("Invalid request payload", 400)

    # Decode token
    try:
        token_data = decode_jwt_token(
            access_token, 
            app.config.get("JWT_ACCESS_SECRET_KEY")
        )
        app.logger.info("Access token successfully validated")
        return success_response(token_data, 200)

    except ExpiredTokenError:
        app.logger.warning("Access token has expired")
        return error_response("Token has expired", 400)
    
    except InvalidTokenError:
        app.logger.warning("Invalid access token")
        return error_response("Invalid token", 400)
    
    except TokenError as err:  # Generic error if any other token issue arises
        app.logger.warning("Error during token validation: %s", str(err))
        return error_response("Invalid or expired token", 400)
    
    except Exception as err:
        app.logger.warning("Unexpected error during token validation: %s", str(err))
        return error_response("Invalid or expired token", 400)
