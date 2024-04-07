from flask import request, jsonify, g
import jwt
from flask import current_app


def jwt_middleware():
    skip_paths = ['/api/auth/v1/login', '/api/auth/v1/signup']  # Public endpoints
    if request.path in skip_paths:
        return  # Allow public routes without JWT
    
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        return jsonify({'error': 'Authorization header missing'}), 401

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify({'error': 'Invalid Authorization header'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, current_app.config.get("JWT_SECRET_KEY"), algorithms=['HS256'])
        g.current_user = payload['sub']  # Save user info in `g` (Flask's global context)

    except jwt.ExpiredSignatureError:
        return jsonify({
                'success': False,
                'error': 'Token expired'
            }), 401
    
    except jwt.InvalidTokenError:
        return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
