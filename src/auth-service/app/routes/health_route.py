from flask import render_template, jsonify, Blueprint, request, g
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from ..core.utils import decode_jwt_token
from flask import current_app


health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/healthz")
def health():

    user = g.current_user
    return jsonify({
        "success": True,
        "logged_as": user,
        "good": "d"
    }), 200
