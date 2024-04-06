from flask import render_template, jsonify, Blueprint, request 
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/api/auth/v1/healthz")
@jwt_required()
def health():

    current_user = get_jwt_identity()
    return jsonify({
        "success": True,
        "logged_as": current_user
    }), 200
