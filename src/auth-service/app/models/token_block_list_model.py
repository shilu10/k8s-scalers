from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ..core.extensions import db 


class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token_hash = db.Column(db.String(128), nullable=False, unique=True)  # Store a hash, not the raw token
    created_at = db.Column(db.DateTime, default=datetime.now)
    revoked = db.Column(db.Boolean, default=False)
