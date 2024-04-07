from flask import jsonify, request, Blueprint
from ..schema.signup_schema import SignUpSchema
from ..services.signup_service import signup_process
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException
from ..core.response_builder import success_response, error_response


signup_bp = Blueprint("signup_bp", __name__)
signup_schema = SignUpSchema()


@signup_bp.route("/api/auth/v1/signup", methods=["POST"])
def signup():
    req_data = request.get_json()

    # Validate schema
    try:
        schema_res = signup_schema.load(req_data)
    except Exception as err:
        return error_response(str(err), 400)

    email = schema_res["email"]
    password = schema_res["password"]

    # Call signup process
    try:
        signup_process_response = signup_process(email, password)
        return jsonify(signup_process_response), 200

    except IntegrityErrorException as e:
        return error_response(str(e), 400)

    except DataErrorException as e:
        return error_response(str(e), 400)

    except OperationalErrorException as e:
        return error_response(str(e), 500)

    except Exception as e:
       return error_response(str(e), 500)
