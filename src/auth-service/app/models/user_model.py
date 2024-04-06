from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..core.extensions import db 


class User(db.Model):
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return  f"User{self.email}"