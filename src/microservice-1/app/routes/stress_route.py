from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
import threading
from ..schema.stress_schema import cpu_mem_stress_schema, mem_stress_schema, cpu_stress_schema
from ..services.stress_service import stress_ng_cpu, stress_ng_mem, stress_ng_cpu_mem


stress_bp = Blueprint("stress_bp", __name__)


@stress_bp.route("/stress_cpu", methods=["POST"])
def increase_stress():
    json_data = request.get_json()

    try:
        data = cpu_stress_schema.load(json_data)

    except ValidationError as err:
        return jsonify(err.messages), 400

    duration = data["duration"]
    workers = data.get("workers", 0)  # number of threads/cores to stress
    load = data["load"]

    if not stress_ng_cpu(workers, duration, load).get("success"):
        return jsonify({
            "message": "internal server error"
        }), 500


    return jsonify({"message": f"CPU stress started for {duration}s using {workers} workers with load {load}"}), 200


@stress_bp.route("/stress_mem", methods=["POST"])
def increase_stress():
    json_data = request.get_json()

    try:
        data = mem_stress_schema.load(json_data)

    except ValidationError as err:
        return jsonify(err.messages), 400

    duration = data["duration"]
    mem_bytes = data["mem_bytes"]

    if not stress_ng_mem(mem_bytes, duration).get("success"):
        return jsonify({
            "message": "internal server error"
        }), 500


    return jsonify({"message": f"Mem stress started for {duration}s  with mem bytes {mem_bytes}"}), 200


@stress_bp.route("/stress_mem_cpu", methods=["POST"])
def increase_stress():
    json_data = request.get_json()

    try:
        data = cpu_mem_stress_schema.load(json_data)

    except ValidationError as err:
        return jsonify(err.messages), 400

    duration = data["duration"]
    mem_bytes = data["mem_bytes"]
    workers = data.get("workers", 0)  # number of threads/cores to stress
    load = data["load"]

    if not stress_ng_cpu_mem(workers, mem_bytes, duration, load).get("success"):
        return jsonify({
            "message": "internal server error"
        }), 500


    return jsonify({"message": f"Mem stress started for {duration}s  with mem bytes {mem_bytes}, and CPU stress started for {duration}s using {workers} workers with load {load}"}), 200