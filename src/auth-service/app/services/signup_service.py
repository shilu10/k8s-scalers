from ..core.extensions import db 
from ..models.user_model import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException
from flask import current_app as app


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
        app.logger.warning("Email already exists or invalid constraints: %s", email)
        raise IntegrityErrorException("Email already exists or invalid constraints") from e

    except DataError as e:
        db.session.rollback()
        app.logger.warning("Provided data is invalid or too large for email: %s", email)
        raise DataErrorException("Provided data is invalid or too large.") from e

    except OperationalError as e:
        db.session.rollback()
        app.logger.warning("Database connection problem for email: %s", email)
        raise OperationalErrorException("Database connection problem. Please try again later.") from e
