from flask import Blueprint, request, jsonify, render_template
from ..services.replica_service import get_replicas_detail


replica_bp = Blueprint('replica_bp', __name__)

@replica_bp.route("/get_all_replicas")
def get_all():
    replicas_detail = get_replicas_detail()
    return jsonify({
        "replicas": replicas_detail
    })
