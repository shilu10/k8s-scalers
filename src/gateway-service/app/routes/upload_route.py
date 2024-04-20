from flask import request, Blueprint, jsonify, g, current_app as app
import requests


upload_bp = Blueprint("upload_route", __name__)


def get_upload_service_url(path: str) -> str:
    """
    Constructs the full URL for the upload service.
    """
    host = app.config.get("UPLOAD_SERVICE")
    port = app.config.get("UPLOAD_SERVICE_PORT")
    return f"http://{host}:{port}{path}"


def forward_to_upload_service(path, payload=None):
    """
    Forwards a POST request to the upload service with user header.
    """
    headers = {
        "X-User-Email": g.current_user
    }

    url = get_upload_service_url(path)
    
    try:
        # Logging before sending the request
        app.logger.info("Forwarding request to %s", url)
        
        response = requests.post(url=url, json=payload, headers=headers)
        
        # Logging response status code
        app.logger.info("Received response from %s: %d", url, response.status_code)
        
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.RequestException as e:
        # Error logging
        app.logger.error(f"Upload Service request failed ({url}): {e}")
        return jsonify({"error": "Upload service unavailable"}), 503
    
    except Exception as e:
        # Generic error logging
        app.logger.exception("Unexpected error in upload gateway")
        return jsonify({"error": "Internal gateway error"}), 500


@upload_bp.route("/upload/generate-presigned-url", methods=["POST"])
def generate_presigned_url():
    """
    Proxy to upload service for generating a presigned S3 URL.
    """
    payload = request.get_json()
    return forward_to_upload_service("/api/v1/generate-presigned-url", payload=payload)


@upload_bp.route("/upload/complete-multipart", methods=["POST"])
def complete_multipart_upload():
    """
    Proxy to upload service for completing a multipart upload.
    """
    payload = request.get_json()
    app.logger.error(f"{payload} payload")
    return forward_to_upload_service("/api/v1/complete-multipart", payload=payload)
