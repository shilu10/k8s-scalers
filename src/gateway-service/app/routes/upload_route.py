from flask import request, Blueprint, jsonify, g
import requests 


upload_bp = Blueprint("upload_route", __name__)

@upload_bp.route("/api/v1/generate-presigned-url", methods=["POST"])
def generate_presigned_url():
    payload = request.get_json()
    headers = {
        "X-User-Email": g.current_user
    }
    
    presigned_url_response = requests.post(
            url="http://upload-service:8002/api/v1/generate-presigned-url",
            json=payload,
            headers=headers
        )
    
    return presigned_url_response.json()