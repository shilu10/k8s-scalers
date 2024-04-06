from flask import render_template, jsonify, request, Blueprint
from ..schema.signup_schema import SignUpSchema
from ..services.signup_service import signup_process


signup_bp = Blueprint("signup_bp", __name__)
signup_schema = SignUpSchema()


@signup_bp.route("/api/auth/v1/signup", methods=["POST"])
def signup():
    req_data = request.get_json()

    try:
        schema_res = signup_schema.load(req_data)

    except Exception as err:
        return jsonify({
            "success": False,
            "message": str(err)
        }), 400

    email = schema_res["email"]
    password = schema_res["password"]

    signup_process_res = signup_process(email, password)

    if not signup_process_res.get("success", False):
        return jsonify({
            "success": False,
            "message": signup_process_res.get("message", "Signup failed.")
        }), 400

    return jsonify({
        "success": True,
        "message": "Signup successful!"
    }), 200

