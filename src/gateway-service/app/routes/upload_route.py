from flask import request, Blueprint, jsonify, g
import requests 
from flask import current_app as app


upload_bp = Blueprint("upload_route", __name__)


@upload_bp.route("/api/v1/generate-presigned-url", methods=["POST"])
def generate_presigned_url():
    payload = request.get_json()
    headers = {
        "X-User-Email": g.current_user
    }
    
    upload_service = app.config.get("UPLOAD_SERVICE")
    upload_service_port = app.config.get("UPLOAD_SERVICE_PORT")

    presigned_url_response = requests.post(
            url=f"http://{upload_service}:{upload_service_port}/api/v1/generate-presigned-url",
            json=payload,
            headers=headers
        )
    
    return presigned_url_response.json()


@upload_bp.route("/api/v1/complete-multipart", methods=["POST"])
def complete_multipart_upload():
    payload = request.get_json()
    headers = {
        "X-User-Email": g.current_user
    }
    
    upload_service = app.config.get("UPLOAD_SERVICE")
    upload_service_port = app.config.get("UPLOAD_SERVICE_PORT")
    
    complete_multipart_upload_response = requests.post(
            url=f"http://{upload_service}:{upload_service_port}/api/v1/complete-multipart",
            json=payload,
            headers=headers
        )
    
    return complete_multipart_upload_response.json()