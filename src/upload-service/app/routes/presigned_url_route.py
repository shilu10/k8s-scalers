from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from ..core.response_builder import success_response, error_response
from ..schema.presigned_url_schema import PreSignedUrlSchema
from ..services.presigned_url_service import generate
from flask import current_app as app
from ..core.errors import ClientErrorException, ValueErrorException


presigned_url_bp = Blueprint("presigned_url_bp", __name__)
presigned_url_schema = PreSignedUrlSchema()


@presigned_url_bp.route("/generate-presigned-url", methods=["POST"])
def generate_presigned_url():
    app.logger.info("Logger initialized successfully.")

    request_data = request.get_json()
    headers = request.headers

    try:
        app.logger.info("Validating schema")
        schema_validation_response = presigned_url_schema.load(request_data)

    except ValidationError as err:
        app.logger.warning("Schema validation error: %s", err)
        return error_response(str(err), 400)

    secured_filename = secure_filename(request_data.get("filename"))
    file_size = request_data.get("filesize")
    app.logger.info("Secured filename: %s", secured_filename)

    try:
        presigned_urls = generate(secured_filename, headers.get("X-User-Email"), file_size)
        return success_response(presigned_urls, 200)

    except ClientErrorException as err:
        app.logger.error("AWS ClientErrorException: %s", err)
        return error_response("Failed to generate presigned URL.", 502)

    except ValueErrorException as err:
        app.logger.error("File size error: %s", err)
        return error_response("File too large or unsupported.", 400)

    except Exception as err:
        app.logger.exception("Unexpected error: %s", err)
        return error_response("Internal server error.", 500)