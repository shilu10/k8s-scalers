from flask import Blueprint, request, jsonify, render_template


health_bp = Blueprint("health_bp",  __name__)

@health_bp.route("/health")
def index():
    return jsonify({
            "success": True
        }), 200