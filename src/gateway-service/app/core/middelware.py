from flask import request, jsonify, g, current_app as app
from .response_builder import error_response
import requests

def jwt_middleware():
    # Skip CORS preflight OPTIONS requests
    if request.method == 'OPTIONS':
        return  # Let Flask-CORS handle it
    
    skip_paths = ['/api/v1/auth/login', '/api/v1/auth/register', '/api/v1/auth/refresh', '/api/v1/auth/logout', '/api/v1/auth/validate', '/api/v1/auth/healthz']
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

    try:
        auth_response = requests.post(
            url="http://auth-service:8001/api/v1/validate-access-token",
            json=data
        )
        auth_payload = auth_response.json()

    except Exception as e:
        app.logger.error("Auth service error: %s", str(e))
        return error_response("Auth service not reachable", 500)

    if auth_payload.get("success"):
        g.current_user = auth_payload["data"]["email"]
        app.logger.info("Token is valid for user: %s", g.current_user)

    else:
        app.logger.warning("Token validation failed: %s", auth_payload.get("error"))
        return error_response(auth_payload.get("error", "Unauthorized"), 401)
