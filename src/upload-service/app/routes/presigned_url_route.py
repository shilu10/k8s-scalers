from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from ..core.response_builder import success_response, error_response
from ..schema.presigned_url_schema import PreSignedUrlSchema
from ..services.presigned_url_service import generate
from flask import current_app as app
from ..core.errors import ClientErrorException, ValueErrorException


# Blueprint registration for presigned URL generation
presigned_url_bp = Blueprint("presigned_url_bp", __name__)

# Instantiate schema for validating incoming data
presigned_url_schema = PreSignedUrlSchema()


@presigned_url_bp.route("/generate-presigned-url", methods=["POST"])
def generate_presigned_url():
    """
    Route for generating a presigned URL to upload a file to S3.
    
    Request Payload (JSON):
    {
        "filename": "<file_name>",
        "filesize": <file_size>
    }
    
    Headers:
    - X-User-Email: <user_email>

    Response:
    - 200 OK: Successful presigned URL generation.
    - 400 Bad Request: Schema validation failure or file size issues.
    - 502 Bad Gateway: AWS client error.
    - 500 Internal Server Error: Unexpected errors.
    """
    
    # Logging request initialization
    app.logger.info("Logger initialized successfully.")

    # Parse the incoming JSON request
    request_data = request.get_json()
    headers = request.headers

    try:
        # Validate the incoming request data with the defined schema
        app.logger.info("Validating schema")
        schema_validation_response = presigned_url_schema.load(request_data)

    except ValidationError as err:
        # Return error response if schema validation fails
        app.logger.warning("Schema validation error: %s", err)
        return error_response(str(err), 400)

    # Secure the file name to prevent security vulnerabilities
    secured_filename = secure_filename(request_data.get("filename"))
    file_size = request_data.get("filesize")
    app.logger.info("Secured filename: %s", secured_filename)

    try:
        # Generate the presigned URL using the service function
        presigned_urls = generate(secured_filename, headers.get("X-User-Email"), file_size)

        # Return the presigned URL in the success response
        return success_response(presigned_urls, 200)

    except ClientErrorException as err:
        # Handle specific AWS S3 ClientErrorException
        app.logger.error("AWS ClientErrorException: %s", err)
        return error_response("Failed to generate presigned URL.", 502)

    except ValueErrorException as err:
        # Handle specific ValueErrorException for file size validation
        app.logger.error("File size error: %s", err)
        return error_response("File too large or unsupported.", 400)

    except Exception as err:
        # Catch any unexpected errors
        app.logger.exception("Unexpected error: %s", err)
        return error_response("Internal server error.", 500)
