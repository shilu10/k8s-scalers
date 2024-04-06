import os 
from .db_uri import generate_db_uri


db_uri = generate_db_uri("mysql", 
                         os.environ["DB_USER"], 
                         os.environ["DB_HOST"], 
                         os.environ["DB_PORT"],
                         os.environ["DB_PASS"],
                         os.environ["DB_NAME"]
                        )

class Config:
    SQLALCHEMY_DATABASE_URI = db_uri
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
