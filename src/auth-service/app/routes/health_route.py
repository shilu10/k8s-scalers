from flask import jsonify, Blueprint
from ..core.response_builder import error_response, success_response


# Create a Blueprint for health check endpoint
health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/healthz", methods=["GET"])
def health():
    """
    Health check endpoint.

    Returns:
        JSON response indicating the health status of the application.
        Example: {"success": True}, HTTP status 200 on success.
    """
    try:
        # You can insert additional health checks here (e.g., DB, cache, etc.)
        return success_response(data="Healthz response", status_code=200)
    
    except Exception as e:
        # Log the error here if you have a logger
        return error_response(message="Internal Server Error", status_code=500)
