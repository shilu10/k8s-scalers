from flask import Blueprint, request, jsonify, render_template


home_bp = Blueprint("home_bp",  __name__)

@home_bp.route("/api/v1")
def index():
    return render_template("index.html")