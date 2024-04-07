from ..core.extensions import db 
from ..models.user_model import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException


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

    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityErrorException("Email already exists or invalid constraints") from e

    except DataError as e:
        db.session.rollback()
        raise DataError("Provided data is invalid or too large.") from e

    except OperationalError as e:
        db.session.rollback()
        raise OperationalError("Database connection problem. Please try again later.") from e 
