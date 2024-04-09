from flask import Flask, request, Blueprint
from ..core.response_builder import success_response, error_response
from ..core.utils import decode_jwt_token
from ..schema.validate_schema import ValidateSchema
from flask import current_app as app


validate_bp = Blueprint("validate_bp", __name__)
validate_schema = ValidateSchema()


@validate_bp.route("/validate-access-token", methods=["POST"])
def validate_token():
    request_data = request.get_json()
    access_token = request_data.get("access_token")

    try:
        schema_validation_response = validate_schema.load(request_data)
        app.logger.info("Validate Schema Validation successfull")

    except Exception as err:
        app.logger.warning("Validate schema validation failed: %s", str(err))
        return error_response(str(err), 400)
    
    try:
        token = decode_jwt_token(access_token,  app.config.get("JWT_ACCESS_SECRET_KEY"))
        return success_response(token, 200)

    except Exception as err:
        return error_response(str(err), 400)

