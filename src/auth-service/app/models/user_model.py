from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ..core.extensions import db


class User(db.Model):
    """
    Model for storing user information in the application.

    This model is used to store the basic information of a user, including their
    email and hashed password for authentication. It is also used to link users 
    to their associated tokens and other resources in the application.

    Fields:
    --------
    id : int
        The primary key for the user record.

    email : str
        The email address of the user, which must be unique. This is typically 
        used as the identifier for the user during authentication.

    password : str
        The hashed password of the user. It is stored securely (hashed) and 
        should be validated before use.

    Relationships:
    --------------
    refresh_tokens : list of RefreshToken
        A one-to-many relationship (if applicable) with the `RefreshToken` model, 
        linking each user to their associated refresh tokens.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        """Returns a string representation of the User instance."""
        return f"User({self.email})"
