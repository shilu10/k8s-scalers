from flask import Blueprint, request, jsonify, render_template
from ..services.cpu_service import get_cpu_usage
from ..services.host_detail_service import get_host_details


cpu_bp = Blueprint("cpu_bp", __name__)

@cpu_bp.route("/cpu")
def cpu_route():
    host_details = get_host_details()
    cpu_usage_details = get_cpu_usage()


    return jsonify({
        "host_details": host_details,
        "cpu_usage_details": cpu_usage_details
    })



