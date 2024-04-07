from sqlalchemy import Column, Integer, String, DateTime, Index
from ..core.extensions import db 


class RevokedToken(db.Model):
    __tablename__ = 'revoked_token'

    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(3000), nullable=False, unique=True)
    expiration_time = db.Column(db.DateTime, nullable=False)

    # Define an index with a prefix length for MySQL
    __table_args__ = (
        Index('ix_refresh_token', 'refresh_token', unique=True, mysql_length=255),  # Use first 255 chars for index
    )

    def __repr__(self):
        return f'<RevokedToken {self.refresh_token}>'