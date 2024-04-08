from flask import request, jsonify, g
import jwt
from flask import request, current_app as app


def jwt_middleware():
    skip_paths = ['/api/v1/login', '/api/v1/signup', '/api/v1/refresh', '/api/v1/logout']  # Public endpoints
    if request.path in skip_paths:
        return  # Allow public routes without JWT
    
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        app.logger.warning("Missing Authorization header at path: %s", request.path)
        return jsonify({'error': 'Authorization header missing'}), 401

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        app.logger.warning("Invalid Authorization header at path: %s", request.path)
        return jsonify({'error': 'Invalid Authorization header'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config.get("JWT_ACCESS_SECRET_KEY"), algorithms=['HS256'])
        g.current_user = payload['sub']  # Save user info in `g` (Flask's global context)

    except jwt.ExpiredSignatureError:
        app.logger.warning("Token Expired")
        return jsonify({
                'success': False,
                'error': 'Token expired'
            }), 401
    
    except jwt.InvalidTokenError:
        app.logger.warning("Invalid token")
        return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
