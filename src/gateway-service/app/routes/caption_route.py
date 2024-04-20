from flask import request, Blueprint, jsonify, g, current_app as app
import requests


caption_bp = Blueprint("caption_bp", __name__)


def get_caption_service_url(path: str) -> str:
    """
    Constructs the full URL for a caption service endpoint.
    """
    host = app.config.get("CAPTION_SERVICE")
    port = app.config.get("CAPTION_SERVICE_PORT")
    return f"http://{host}:{port}{path}"


def forward_to_caption_service(method, path, payload=None, headers=None):
    """
    Forwards a request to the caption service.

    Args:
        method (str): HTTP method, e.g., 'POST' or 'GET'.
        path (str): The API path on the caption service.
        payload (dict): Request body (for POST).
        headers (dict): Request headers.

    Returns:
        Flask Response: JSON response with status code.
    """
    url = get_caption_service_url(path)
    try:
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error connecting to Caption Service at {url}: {e}")
        return jsonify({"error": "Caption service unavailable"}), 503
    
    except Exception as e:
        app.logger.exception("Unhandled error in caption gateway")
        return jsonify({"error": "Internal gateway error"}), 500


@caption_bp.route("/caption/request", methods=["POST"])
def request_caption():
    """
    Proxy endpoint to request a new caption job.
    """
    payload = request.get_json()
    current_user = g.current_user

    headers = {
        "X-User-Email": current_user
    }

    return forward_to_caption_service(
        method="POST",
        path="/api/v1/caption/request",
        payload=payload,
        headers=headers
    )


@caption_bp.route("/caption/status/<job_id>", methods=["GET"])
def caption_status(job_id):
    """
    Proxy endpoint to get status of a caption job.
    """
    headers = {
        "X-User-Email": g.current_user
    }

    return forward_to_caption_service(
        method="GET",
        path=f"/api/v1/caption/status/{job_id}",
        headers=headers
    )


@caption_bp.route("/caption/result/<job_id>", methods=["GET"])
def caption_result(job_id):
    """
    Proxy endpoint to get result (transcript) of a caption job.
    """
    headers = {
        "X-User-Email": g.current_user
    }

    return forward_to_caption_service(
        method="GET",
        path=f"/api/v1/caption/result/{job_id}",
        headers=headers
    )
