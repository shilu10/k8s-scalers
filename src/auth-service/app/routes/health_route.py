from flask import render_template, jsonify, Blueprint, request, g
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from ..core.utils import decode_jwt_token
from flask import current_app


health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/api/auth/v1/healthz")
#@jwt_required()
def health():
    #auth_header = request.headers.get('Authorization', None)
    #if not auth_header: 
     #   return jsonify({
      #      "success": False,
       #     "reason": "No Authorization Token provided."
        #})
    
    #token = auth_header.split(' ')[1]
    #decode_response = decode_jwt_token(token, current_app.config.get("JWT_SECRET_KEY"))

    #if not decode_response.get("success"):
     #   return jsonify({
      #      "success": False,
       #     "reason": decode_response.get("reason")
        #})

    user = g.current_user
    return jsonify({
        "success": True,
        "logged_as": user,
        "good": "d"
    }), 200
