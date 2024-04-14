from flask import Blueprint, jsonify
from ..core.response_builder import error_response, success_response


# Define a blueprint for health check routes
healthz_bp = Blueprint("healthz_route", __name__)

@healthz_bp.route("/healthz")
def health():
    """
    Health check endpoint.

    Returns:
        JSON response indicating service is healthy.
    """
    try:
        # Health check logic (can be extended)
        return success_response(data="Healthz route success", status_code=200)
    
    except Exception as e:
        # In case any error occurs (rare in healthz, but for completeness)
        return error_response(message="Healthz route failed", status_code=500)