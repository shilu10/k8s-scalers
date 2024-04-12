from flask import request, Blueprint, jsonify
import requests 
from flask import current_app as app


auth_bp = Blueprint("auth_route", __name__)

@auth_bp.route("/api/v1/login", methods=["POST"])
def login():
    payload = request.get_json()

    auth_service_host = app.config.get("AUTH_SERVICE")
    auth_service_port = app.config.get("AUTH_SERVICE_PORT")

    auth_service_response = requests.post(
                                url=f"http://{auth_service_host}:{auth_service_port}/api/v1/login",
                                json=payload
                            )
    
    return auth_service_response.json()


@auth_bp.route("/api/v1/register", methods=["POST"])
def register():
    payload = request.get_json()

    auth_service_host = app.config.get("AUTH_SERVICE")
    auth_service_port = app.config.get("AUTH_SERVICE_PORT")
    auth_service_response = requests.post(
                                url=f"http://{auth_service_host}:{auth_service_port}/api/v1/signup",
                                json=payload
                            )
    
    return auth_service_response.json()


@auth_bp.route("/api/v1/refresh", methods=["POST"])
def refresh():
    payload = request.get_json()
    headers = request.headers

    auth_service_host = app.config.get("AUTH_SERVICE")
    auth_service_port = app.config.get("AUTH_SERVICE_PORT")
    auth_service_response = requests.post(
                                url=f"http://{auth_service_host}:{auth_service_port}/api/v1/refresh",
                                json=payload,
                                headers=headers
                            )
    
    return auth_service_response.json()


@auth_bp.route("/api/v1/logout", methods=["GET"])
def healthz():
    payload = request.get_json()

    auth_service_host = app.config.get("AUTH_SERVICE")
    auth_service_port = app.config.get("AUTH_SERVICE_PORT")
    auth_service_response = requests.post(
                                url=f"http://{auth_service_host}:{auth_service_port}/api/v1/logout",
                                json=payload,
                            )
    
    return auth_service_response.json()