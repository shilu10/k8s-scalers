from flask import Blueprint, request, jsonify, current_app as app
from botocore.exceptions import ClientError
from ..core.s3 import get_s3_client
from ..services.multipart_complete_service import complete_multipart_upload
import os
from ..core.response_builder import error_response, success_response


multipart_complete_bp = Blueprint('multipart_complete_bp', __name__)


@multipart_complete_bp.route('/complete-multipart', methods=['POST'])
def complete_multipart_upload_api():
    try:
        data = request.get_json()
        headers = request.headers

        app.logger.info(data, headers)

        # Extract required fields
        upload_id = data.get('uploadId')
        file_name = data.get('filename')
        parts = data.get('parts')  # List of { ETag, PartNumber }
        email = headers.get('X-User-Email')

        app.logger.info("Started Multipart complete")

        # Basic validation
        if not all([upload_id, file_name, parts, email]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Optional: Confirm user is authorized to upload for this path
        object_path = os.path.join(email, file_name)
        bucket_name = app.config.get("OBJECT_STORE_BUCKET_NAME")
        s3_client = get_s3_client()

        # Ensure ETags are properly quoted (AWS expects this)
        for part in parts:
            etag = part.get("ETag")
            if etag and not etag.startswith('"'):
                part["ETag"] = f'"{etag}"'

        # Attempt to complete the upload
        result = complete_multipart_upload(
            s3_client=s3_client,
            bucket_name=bucket_name,
            object_path=object_path,
            upload_id=upload_id,
            parts=parts
        )

        file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_path}"

        data = {
            "message": "Upload Completed successfully.",
            "fileUrl": file_url,
            "result": result
        }
        return success_response(data, 200)

    except ClientError as e:
        app.logger.exception("AWS ClientError during multipart completion")
        return error_response("AWS S3 error during upload completion.", 502)

    except Exception as e:
        app.logger.exception("Unexpected error during multipart completion")
        return error_response("Internal server error during upload completion.", 502)
