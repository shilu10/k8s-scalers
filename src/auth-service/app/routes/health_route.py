from flask import render_template, jsonify, Blueprint, request 


health_bp = Blueprint("health_bp", __name__)

@health_bp.route("/api/auth/v1/healthz")
def health():
    return jsonify({
        "success": True 
    }), 200
