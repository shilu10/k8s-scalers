from flask import Blueprint, request, jsonify, render_template


home_bp = Blueprint("home_bp")

@home_bp.route("/")
def index():
    jsonify(
        {
            "success": True
        }
    )