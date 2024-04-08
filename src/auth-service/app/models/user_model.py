from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ..core.extensions import db 


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return  f"User{self.email}"