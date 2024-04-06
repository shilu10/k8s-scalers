from werkzeug.security import check_password_hash
from ..models.user_model import User
from ..core.extensions import db

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
        password_verification_res = check_password_hash(user.password, password)

        # If password verification fails
        if not password_verification_res:
            return {
                "success": False,
                "reason": "Invalid password."
            }

        # If everything is correct
        return {
            "success": True,
            "message": "Login successful!"
        }

    except Exception as err:
        # Handle unexpected errors
        return {
            "success": False,
            "reason": str(err)
        }
