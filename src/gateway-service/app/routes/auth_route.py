from flask import request, Blueprint, jsonify
import requests
from flask import current_app as app


auth_bp = Blueprint("auth_route", __name__)


def get_auth_service_url(path: str) -> str:
    """
    Builds the full URL for a given Auth Service path.
    """
    host = app.config.get("AUTH_SERVICE")
    port = app.config.get("AUTH_SERVICE_PORT")
    
    return f"http://{host}:{port}{path}"


def forward_request_to_auth(path, method="POST", payload=None, headers=None):
    """
    Forwards request to the Auth Service and handles errors.

    Args:
        path (str): Path on the auth service to call.
        method (str): HTTP method, default is POST.
        payload (dict): JSON body.
        headers (dict): Headers to forward (for token refresh etc.)

    Returns:
        Flask Response (JSON)
    """
    url = get_auth_service_url(path)
    try:
        response = requests.request(method=method, url=url, json=payload, headers=headers)
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to connect to Auth Service at {url}: {e}")
        return jsonify({"error": "Authentication service unavailable"}), 503
    
    except Exception as e:
        app.logger.exception("Unhandled error in gateway auth route")
        return jsonify({"error": "Internal gateway error"}), 500


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Forwards login request to the Auth Service.
    """
    payload = request.get_json()
    return forward_request_to_auth("/api/v1/login", payload=payload)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """
    Forwards registration request to the Auth Service.
    """
    payload = request.get_json()
    return forward_request_to_auth("/api/v1/signup", payload=payload)


@auth_bp.route("/auth/refresh", methods=["POST"])
def refresh():
    """
    Forwards token refresh request to the Auth Service.
    """
    payload = request.get_json()
    return forward_request_to_auth("/api/v1/refresh", payload=payload, headers=request.headers)


@auth_bp.route("/auth/logout", methods=["POST"])  # Changed from GET to POST
def logout():
    """
    Forwards logout request to the Auth Service.
    """
    payload = request.get_json()
    return forward_request_to_auth("/api/v1/logout", payload=payload)


@auth_bp.route("/auth/healthz", methods=["GET"])  # Changed from GET to POST
def home():
    """
    Forwards logout request to the Auth Service.
    """
    payload = request.get_json()
    return forward_request_to_auth("/api/v1/healthz", payload=payload)