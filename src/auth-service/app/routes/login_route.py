from flask import render_template, jsonify, request, Blueprint 
from ..schema.login_schema import LoginSchema
from ..services.login_service import login_process
from flask_cors import CORS



login_bp = Blueprint("login_bp", __name__)
CORS(login_bp, origins=["http://localhost:3000", "https://yourfrontend.com"])

login_schema = LoginSchema()

@login_bp.route("/api/auth/v1/login", methods=["POST"])
def login():
    login_data = request.get_json()
    try:
        res = login_schema.load(login_data)
    
    except Exception as err:
        return jsonify({
            "success": False,
            "message": str(err)
        }), 400

    # login process
    login_validation = login_process(res["email"], res["password"])

    if not login_validation.get("success"):
        return jsonify({
            "success": False,
            "message": login_validation.get("reason")
        }), 400
    

    return jsonify({
        "success": True,
    }), 200