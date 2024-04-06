from werkzeug.security import check_password_hash
from ..models.user_model import User
from ..core.extensions import db
from flask_jwt_extended import create_access_token


def check_password(user_password, current_password):
    verification_res = check_password_hash(user_password, current_password)

    return verification_res


def login_process(email, password):
    try:
        # Query user by email
        user = db.session.query(User).filter_by(email=email).first()

        # If user doesn't exist
        if user is None:
            return {
                "success": False,
                "reason": "User not found."
            }

        # Check password hash
        password_verification_res = check_password(user.password, password)

        # If password verification fails
        if not password_verification_res:
            return {
                "success": False,
                "reason": "Invalid password."
            }

        # If everything is correct
        access_token = create_access_token(identity=email)
        return {
            "success": True,
            "message": "Login successful!",
            "access_token": access_token
        }

    except Exception as err:
        # Handle unexpected errors
        return {
            "success": False,
            "reason": str(err)
        }
