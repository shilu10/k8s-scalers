from flask import Blueprint, request, jsonify, render_template
from flask import current_app as app


health_bp = Blueprint("health_bp", __name__)

@health_bp.route("/healthz")
def index():
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
