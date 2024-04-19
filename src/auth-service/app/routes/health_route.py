from flask import Blueprint, request, jsonify, Response
from flask import current_app as app
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Summary
import random, time


health_bp = Blueprint("health_bp", __name__)
REQUESTS_PER_SECOND = Summary('requests_per_second', 'Custom RPS metric')


@REQUESTS_PER_SECOND.time()
@health_bp.route("/healthz")
def health():
    """
    Health check endpoint that checks the status of the application.
    
    ---
    Returns:
    - 200 OK: Indicates the application is running correctly.
    - 500 Internal Server Error: If any unexpected error occurs.
    """
    try:
        # Log health check request
        app.logger.info("Healthz route called.")
        
        # Check application health (for more complex systems, this can include DB, Redis checks, etc.)
        # For simplicity, we assume the application is healthy if this route is hit successfully.
        return jsonify({"success": True}), 200

    except Exception as e:
        # Catch any unexpected errors
        app.logger.error(f"Unexpected error during health check: {str(e)}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500


@health_bp.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)