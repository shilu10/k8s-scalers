from flask import render_template, jsonify, request, Blueprint, abort 
from ..schema.login_schema import LoginSchema
from ..services.login_service import login_process
from flask_cors import CORS
from ..core.errors import AuthErrorException
from ..core.response_builder import success_response, error_response
from flask import current_app as app 


login_bp = Blueprint("login_bp", __name__)
login_schema = LoginSchema()


@login_bp.route("/api/auth/v1/login", methods=["POST"])
def login():
    login_data = request.get_json()
    app.logger.info("Login attempt with email: %s", login_data.get("email"))

    try:
        res = login_schema.load(login_data)
    
    except Exception as err:
        app.logger.error("Login schema validation failed: %s", str(err))
        return error_response(str(err), 400)

    # login process
    try:
        login_process_response = login_process(res["email"], res["password"])
        app.logger.info("Login attempt succeeded for email: %s", login_data.get("email"))

        return success_response("Loggedin Successfully...")
    
    except AuthErrorException as err:
        app.logger.warning("Login attempt failed for email: %s", login_data.get("email"))
        return error_response(str(err), 400)