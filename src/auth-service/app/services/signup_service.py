from ..core.extensions import db
from ..models.user_model import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from ..core.errors import IntegrityErrorException, DataErrorException, OperationalErrorException, ValidationErrorException
from flask import current_app as app
from ..core.publish_event_sns import publish_event
import botocore.exceptions

def get_password_hash(password):
    """
    Generates a hashed password using the werkzeug.security generate_password_hash function.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed password.
    """
    hashed_password = generate_password_hash(password)
    return hashed_password


def signup_process(email, password):
    """
    Handles the process of signing up a new user. The user's email and password are saved in the database after 
    validating the data and hashing the password. An SNS event is also published to notify about the new user creation.

    Args:
        email (str): The email address of the user.
        password (str): The plain-text password of the user.

    Returns:
        dict: A dictionary containing a success message and a flag indicating success.

    Raises:
        IntegrityErrorException: Raised if the email already exists in the database or if there are any constraint violations.
        DataErrorException: Raised if the provided data is invalid or too large for the database.
        OperationalErrorException: Raised if there is an operational issue with the database connection.
        ValidationErrorException: Raised if there is a validation failure during the SNS event publication.
        Exception: Raised for any unexpected errors.
    """
    try:
        # Create a new user object with the provided email and hashed password
        user = User(
            email=email,
            password=get_password_hash(password)
        )

        # Add the user to the session
        db.session.add(user)

        # Publish an event to SNS (Simple Notification Service) about the new user creation
        topic_arn = app.config.get("TOPIC_ARN")
        message = dict()
        message["email"] = email
        
        # Handle SNS event publishing and capture any potential error
        try:
            response = publish_event(topic_arn=topic_arn, message=message)
            app.logger.info("Successfully pushed event to SNS topic for email: %s", email)
            
        except botocore.exceptions.ClientError as sns_error:
            app.logger.warning("SNS publish failed for email %s: %s", email, sns_error)
            raise ValidationErrorException("SNS event publishing failed.") from sns_error
        
        # Commit the transaction to the database
        db.session.commit()
        app.logger.info("User created successfully for email: %s", email)

        return {
            "success": True,
            "message": "User created successfully!"
        }

    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning("Email already exists or invalid constraints for email: %s, Error: %s", email, str(e))
        raise IntegrityErrorException("Email already exists or invalid constraints") from e

    except DataError as e:
        db.session.rollback()
        app.logger.warning("Provided data is invalid or too large for email: %s, Error: %s", email, str(e))
        raise DataErrorException("Provided data is invalid or too large.") from e

    except OperationalError as e:
        db.session.rollback()
        app.logger.warning("Database connection problem for email: %s, Error: %s", email, str(e))
        raise OperationalErrorException("Database connection problem. Please try again later.") from e

    except ValidationErrorException as e:
        db.session.rollback()
        app.logger.warning("Validation failed during SNS topic publish for email: %s, Error: %s", email, str(e))
        raise ValidationErrorException("Validation failed during SNS event publication.") from e

    except Exception as e:
        db.session.rollback()
        app.logger.warning("Unknown error occurred during signup for email: %s, Error: %s", email, str(e))
        raise Exception("An unknown error occurred during the signup process.") from e
