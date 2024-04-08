from flask import render_template, jsonify, request, Blueprint, abort 
from ..schema.login_schema import LoginSchema
from ..services.login_service import login_process
from ..core.errors import AuthErrorException, DataErrorException, OperationalErrorException, IntegrityErrorException
from ..core.response_builder import success_response, error_response
from flask import current_app as app 
from ..core.extensions import db 


login_bp = Blueprint("login_bp", __name__)
login_schema = LoginSchema()


@login_bp.route("/login", methods=["POST"])
def login():
    login_data = request.get_json()
    email = login_data.get("email")
    app.logger.info("Login attempt with email: %s", email)

    try:
        res = login_schema.load(login_data)
    
    except Exception as err:
        app.logger.error("Login schema validation failed: %s", str(err))
        return error_response(str(err), 400)

    # login process
    try:
        access_token, refresh_token = login_process(res["email"], res["password"])
        app.logger.info("Login attempt succeeded for email: %s", email)

        return success_response(data={"access_token": access_token, 
                                     "refresh_token": refresh_token
                                    })
    
    except IntegrityErrorException as err:
        app.logger.info("Login Process failed due to Integrity error for email: %s", email)
        return error_response(str(err), 500)
    
    except DataErrorException as err:
        app.logger.info("Login Process failed due to data error for email: %s", email)
        return error_response(str(err), 500)
    
    except OperationalErrorException as err:
        app.logger.info("Login Process failed due to operational error for email: %s", email)
        return error_response(str(err), 500)
    
    except AuthErrorException as err:
        app.logger.warning("Login attempt failed for email: %s", email)
        return error_response(str(err), 400)
    




    


