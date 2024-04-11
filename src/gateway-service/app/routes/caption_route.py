from flask import request, Blueprint, jsonify, g
import requests


caption_bp = Blueprint("caption_bp", __name__)


@caption_bp.route("/api/v1/request", methods=["POST"])
def request_caption():
    payload = request.get_json()
    current_user = g.current_user

    headers = {
        "X-User-Email": current_user
    }

    caption_service_response = requests.post(
                                url="http://caption-service:5000/api/v1/request",
                                json=payload, 
                                headers=headers
                            )
    
    return caption_service_response.json()