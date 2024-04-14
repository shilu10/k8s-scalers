from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
import threading
from ..schema.stress_schema import cpu_mem_stress_schema, mem_stress_schema, cpu_stress_schema
from ..services.stress_service import stress_ng_cpu, stress_ng_mem, stress_ng_cpu_mem


stress_bp = Blueprint("stress_bp", __name__)

"""
Blueprint for handling CPU, Memory, and CPU+Memory stress testing routes.

This Blueprint contains the following routes:
- /api/v1/stress_cpu: To initiate a CPU stress test.
- /api/v1/stress_mem: To initiate a memory stress test.
- /api/v1/stress_mem_cpu: To initiate both CPU and memory stress tests simultaneously.

Each route performs schema validation on the incoming request data and starts the appropriate stress test
using the stress_ng tool. In case of success, a message is returned, and in case of failure, an error message
with an appropriate HTTP status code is returned.
"""

@stress_bp.route("/stress_cpu", methods=["POST"])
def stress_cpu():
    """
    Endpoint to initiate a CPU stress test.

    This route accepts a POST request with JSON data to perform CPU stress testing.
    
    Request JSON:
    {
        "duration": <int>,  # Duration in seconds for the stress test
        "workers": <int>,   # Number of CPU cores to stress (optional, default: 0)
        "load": <int>       # Load percentage for CPU stress (e.g., 70 for 70% load)
    }

    Response:
    - On success: Returns a message indicating the stress test has started.
    - On failure: Returns an error message with status code 500 if the test fails to start.

    Returns:
        jsonify: Response with a success or failure message.
    """
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
def stress_mem():
    """
    Endpoint to initiate a memory stress test.

    This route accepts a POST request with JSON data to perform memory stress testing.
    
    Request JSON:
    {
        "duration": <int>,       # Duration in seconds for the stress test
        "mem_bytes": <int>,      # Amount of memory (in bytes) to allocate for stress
        "vm_workers": <int>      # Number of virtual memory workers
    }

    Response:
    - On success: Returns a message indicating the memory stress test has started.
    - On failure: Returns an error message with status code 500 if the test fails to start.

    Returns:
        jsonify: Response with a success or failure message.
    """
    json_data = request.get_json()

    try:
        data = mem_stress_schema.load(json_data)

    except ValidationError as err:
        return jsonify(err.messages), 400

    duration = data["duration"]
    mem_bytes = data["mem_bytes"]
    vm_workers = data["vm_workers"]

    stress_result = stress_ng_mem(mem_bytes, duration, vm_workers=vm_workers)
    if not stress_result.get("success"):
        return jsonify({
            "message": stress_result.get("err")
        }), 500

    return jsonify({"message": f"Mem stress started for {duration}s  with mem bytes {mem_bytes}"}), 200


@stress_bp.route("/stress_mem_cpu", methods=["POST"])
def stress_mem_cpu():
    """
    Endpoint to initiate both CPU and memory stress tests.

    This route accepts a POST request with JSON data to perform both CPU and memory stress testing simultaneously.
    
    Request JSON:
    {
        "duration": <int>,        # Duration in seconds for both stress tests
        "mem_bytes": <int>,       # Amount of memory (in bytes) to allocate for stress
        "workers": <int>,         # Number of CPU cores to stress (optional, default: 0)
        "load": <int>,            # Load percentage for CPU stress (e.g., 70 for 70% load)
        "vm_workers": <int>       # Number of virtual memory workers
    }

    Response:
    - On success: Returns a message indicating both CPU and memory stress tests have started.
    - On failure: Returns an error message with status code 500 if the test fails to start.

    Returns:
        jsonify: Response with a success or failure message.
    """
    json_data = request.get_json()

    try:
        data = cpu_mem_stress_schema.load(json_data)

    except ValidationError as err:
        return jsonify(err.messages), 400

    duration = data["duration"]
    mem_bytes = data["mem_bytes"]
    workers = data.get("workers", 0)  # number of threads/cores to stress
    load = data["load"]
    vm_workers = data["vm_workers"]

    if not stress_ng_cpu_mem(workers, mem_bytes, vm_workers, duration, load).get("success"):
        return jsonify({
            "message": "internal server error"
        }), 500

    return jsonify({"message": f"Mem stress started for {duration}s  with mem bytes {mem_bytes}, and CPU stress started for {duration}s using {workers} workers with load {load}"}), 200
