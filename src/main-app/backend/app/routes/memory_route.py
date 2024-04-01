from flask import Blueprint, request, jsonify, render_template
from ..services.memory_service import get_memory_usage
from ..services.host_detail_service import get_host_details


memory_bp = Blueprint("memory_bp", __name__)

@memory_bp.route("/memory")
def cpu_route():
    host_details = get_host_details()
    memory_usage_details = get_memory_usage()


    return jsonify({
        "host_details": host_details,
        "memory_usage_details": memory_usage_details
    })



