from ..core.extensions import db 
from ..models.user_model import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, DataError, OperationalError


def get_password_hash(password):
    hashed_password = generate_password_hash(password)
    
    return hashed_password


def signup_process(email, password):
    try:
        user = User(
            email=email,
            password=get_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return {
            "success": True,
            "message": "User created successfully!"
        }

    except IntegrityError:
        db.session.rollback()
        return {
            "success": False,
            "message": "An unexpected error occurred. Please try again later."
        }

    except DataError:
        db.session.rollback()
        return {
            "success": False,
            "message": "Provided data is invalid or too large."
        }

    except OperationalError:
        db.session.rollback()
        return {
            "success": False,
            "message": "Database connection problem. Please try again later."
        }

    except Exception as err:
        db.session.rollback()
        return {
            "success": False,
            "message": f"Unexpected error: {str(err)}"
        }
