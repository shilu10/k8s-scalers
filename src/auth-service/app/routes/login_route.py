from flask import render_template, jsonify, request, Blueprint, abort 
from ..schema.login_schema import LoginSchema
from ..services.login_service import login_process
from flask_cors import CORS
from ..core.errors import AuthErrorException
from ..core.response_builder import success_response, error_response
from flask import current_app as app 
from ..core.utils import decode_jwt_token, generate_access_token


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
        access_token, refresh_token = login_process(res["email"], res["password"])
        app.logger.info("Login attempt succeeded for email: %s", login_data.get("email"))

        return success_response(data={"access_token": access_token, 
                                     "refresh_token": refresh_token
                                    })
    
    except AuthErrorException as err:
        app.logger.warning("Login attempt failed for email: %s", login_data.get("email"))
        return error_response(str(err), 400)
    

@login_bp.route("/api/auth/v1/refresh", methods=["POST"])
def refresh():
    try:
        request_data = request.get_json()
        authorization_header = request.headers.get('Authorization', None)

        refresh_token = None

        # Priority: Authorization header -> body
        if authorization_header:
            if authorization_header.startswith("Bearer "):
                refresh_token = authorization_header.split(" ")[1]
            else:
                refresh_token = authorization_header

        elif request_data and request_data.get("refresh_token"):
            refresh_token = request_data.get("refresh_token")

        if not refresh_token:
            return error_response("No Refresh Token found", 400)

        # Decode refresh token
        payload = decode_jwt_token(refresh_token, app.config.get("JWT_REFRESH_SECRET_KEY"))
        
        user_id = payload["sub"]
        email = payload["email"]
        
        app.logger.info("Refresh attempt with email: %s", email)

        # Generate new access token (valid for 15 minutes)
        access_token = generate_access_token(user_id, email, app.config.get("JWT_ACCESS_SECRET_KEY"), 1)

        app.logger.info("Generated new access token for email: %s", email)

        return success_response({"access_token": access_token})

    except Exception as err:
        # In error, don't assume payload exists
        app.logger.warning("Refresh attempt failed. Reason: %s", str(err))
        return error_response(str(err), 400)







    


