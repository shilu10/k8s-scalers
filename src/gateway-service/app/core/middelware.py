from flask import request, jsonify, g
import jwt
from flask import request, current_app as app
from .response_builder import error_response, success_response
import requests


def jwt_middleware():
    skip_paths = ['/api/v1/login', '/api/v1/signup', '/api/v1/refresh', '/api/v1/logout', '/api/v1/validate']  # Public endpoints
    if request.path in skip_paths:
        return  # Allow public routes without JWT
    
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        app.logger.warning("Missing Authorization header at path: %s", request.path)
        return error_response('Authorization header missing', 401)

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        app.logger.warning("Invalid Authorization header at path: %s", request.path)
        return error_response('Invalid Authorization header', 401)

    token = parts[1]
    data = {
        "access_token": token
    }
    
    auth_response = requests.post(
            url = "http://auth-service:8001/api/v1/validate-access-token",
            json=data
    )
    auth_payload = auth_response.json()
    if auth_payload["success"]:
        current_user = auth_payload["data"]["sub"]
        g.current_user = current_user  # Save user info in `g` (Flask's global context)
        app.logger.info("Token is Valid of user: %s", current_user)

    else:
        app.logger.warning(auth_payload["error"])
        return error_response(auth_payload["error"], 401)


