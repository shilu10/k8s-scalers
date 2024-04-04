from flask import render_template, jsonify, Blueprint
from ..services.rabbitmq_service import consume_message 


consumer_bp = Blueprint("consumer_bp", __name__)




