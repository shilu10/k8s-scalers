import os
from flask import Blueprint, request, jsonify, current_app as app
from botocore.exceptions import ClientError
from marshmallow import ValidationError
from ..core.s3 import get_s3_client
from ..services.multipart_complete_service import complete_multipart_upload
from ..core.response_builder import error_response, success_response
from ..schema.multipart_complete_schema import MultiPartCompleteSchema


multipart_complete_bp = Blueprint('multipart_complete_bp', __name__)

multipart_complete_schema = MultiPartCompleteSchema()


@multipart_complete_bp.route('/complete-multipart', methods=['POST'])
def complete_multipart_upload_api():
    """
    Complete the multipart upload by combining all uploaded parts in S3.
    
    ---
    Request JSON:
    {
        "uploadId": "<upload_id>",
        "filename": "<file_name>",
        "parts": [
            {"PartNumber": <part_number>, "ETag": "<etag>"}, 
            ...
        ]
    }
    
    Request Headers:
    - X-User-Email: <user_email>
    
    Returns:
    - 200 OK: Upload completed successfully with file URL.
    - 400 Bad Request: Missing required fields or invalid input.
    - 502 Bad Gateway: AWS error or internal server issue.
    """
    # Parse JSON request body and headers
    data = request.get_json()
    headers = request.headers

    app.logger.info(f"Received request data: {data}, headers: {headers}")

    # Validate schema
    try:
        validated_data = multipart_complete_schema.load(data)

    except ValidationError as err:
        app.logger.warning(f"Validation error: {err.messages}")
        return jsonify({"success": False, "message": err.messages}), 400

    # Extract validated fields
    upload_id = validated_data.get('uploadId')
    file_name = validated_data.get('filename')
    parts = validated_data.get('parts')  # List of { PartNumber, ETag }
    email = headers.get('X-User-Email')

    app.logger.info("Starting multipart upload completion")

    # Construct object path and prepare S3 client
    object_path = os.path.join(email, file_name)
    bucket_name = app.config.get("OBJECT_STORE_BUCKET_NAME")
    s3_client = get_s3_client()

    # Ensure ETags are properly quoted (AWS expects this format)
    for part in parts:
        etag = part.get("ETag")
        if etag and not etag.startswith('"'):
            part["ETag"] = f'"{etag}"'

    # Call service to complete the multipart upload
    try:
        result = complete_multipart_upload(
            s3_client=s3_client,
            bucket_name=bucket_name,
            object_path=object_path,
            upload_id=upload_id,
            parts=parts
        )
        
    except ClientError as e:
        # Handle AWS ClientError (e.g., S3 error)
        app.logger.exception("AWS ClientError during multipart completion")
        return error_response("AWS S3 error during upload completion.", 502)

    # Construct the URL to the uploaded file
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_path}"

    # Return success response
    data = {
        "message": "Upload completed successfully.",
        "fileUrl": file_url,
        "result": result
    }
    return success_response(data, 200)
