from flask import Blueprint, jsonify, render_template, request
from marshmallow import ValidationError
from .schema.message_schema import MessageSchema


producer_bp = Blueprint("producer_bp")
message_schema = MessageSchema()


@producer_bp.route("/post_message", methods=["POST"])
def post_message():
    json_data = request.get_json()

    try:
        data = message_schema.load(json_data)


    except ValidationError as err:
        return jsonify(err.messages), 400
    
    return jsonify(
        "message": "success"
    ), 200
