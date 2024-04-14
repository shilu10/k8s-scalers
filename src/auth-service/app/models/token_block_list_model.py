from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ..core.extensions import db


class RefreshToken(db.Model):
    """
    Model for storing refresh tokens in the application.

    This model is used to store the refresh tokens for users. A refresh token is 
    used to issue new access tokens when the old ones expire. The refresh token 
    is stored as a hashed value for security reasons.

    Fields:
    --------
    id : int
        The primary key for the refresh token entry.
    
    user_id : int
        The user ID associated with the refresh token.
    
    token_hash : str
        The hashed value of the refresh token (for security purposes).
    
    created_at : datetime
        The timestamp when the refresh token was created.
    
    revoked : bool
        A flag indicating whether the refresh token has been revoked. Default is False.

    Relationships:
    --------------
    user : User
        The user who owns the refresh token. (Assumes a one-to-one or one-to-many relationship with the User model.)
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token_hash = db.Column(db.String(128), nullable=False, unique=True)  # Store a hash, not the raw token
    created_at = db.Column(db.DateTime, default=datetime.now)
    revoked = db.Column(db.Boolean, default=False)

    # Optional: relationship to User model, assuming one-to-many or one-to-one
    # user = db.relationship('User', backref='refresh_tokens', lazy=True)

    def __repr__(self):
        """Returns a string representation of the refresh token (for debugging purposes)."""
        return f'<RefreshToken {self.token_hash}>'

    def revoke(self):
        """Marks the refresh token as revoked."""
        self.revoked = True
        db.session.commit()

    def is_revoked(self):
        """Checks if the refresh token is revoked."""
        return self.revoked
