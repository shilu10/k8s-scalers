from flask import Blueprint, jsonify, request 
from flask_cors import CORS 
from flask_jwt_extended import unset_jwt_cookies
from ..services.logout_service import logout_user


logout_bp = Blueprint("logout_bp", __name__)
CORS(logout_bp, origins=["http://localhost:3000", "https://yourfrontend.com"])

@logout_bp.route("/api/auth/v1/logout")
def logout_with_cookies():
    try:
        response = jsonify({"message": "logout successful"})
        logout_res = logout_user(response)

        return response, 200

    except Exception as err:
        return jsonify({
            "message": "logout unsuccessful"
        }), 500
