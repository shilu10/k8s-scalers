from flask import Blueprint, jsonify, render_template, request
from marshmallow import ValidationError
from .schema.stress_schema import StressSchema


stress_bp = Blueprint("stress_bp")
stress_schema = StressSchema()


@stress_bp.route("/increase_stress", methods=["POST"])
def increase_stress():
    json_data = request.get_json()

    try:
        data = stress_schema.load(json_data)

    except ValidationError as err:
        return jsonify(err.message), 400
    
    return jsonify(
        {
            "message": "success"
        }
    ), 200


