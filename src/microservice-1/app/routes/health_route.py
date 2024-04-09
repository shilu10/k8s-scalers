from flask import Blueprint, request, jsonify, render_template
from flask import current_app as app

health_bp = Blueprint("health_bp",  __name__)

@health_bp.route("/api/v1/healthz")
def index():
    app.logger.info("logged")
    return jsonify({
            "success": True
        }), 200