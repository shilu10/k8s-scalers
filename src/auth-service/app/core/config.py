import os 
from .db_uri import generate_db_uri


db_uri = generate_db_uri("mysql", 
                         os.environ["DB_USER"], 
                         os.environ["DB_HOST"], 
                         int(os.environ["DB_PORT"]),
                         os.environ["DB_PASS"],
                         os.environ["DB_NAME"]
                        )

class Config:
    SQLALCHEMY_DATABASE_URI = db_uri
    JWT_ACCESS_SECRET_KEY = os.environ["JWT_ACCESS_SECRET_KEY"]
    LOG_DIR = os.environ["LOG_DIR"]
    JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXP_MIN = int(os.environ.get("JWT_ACCESS_TOKEN_EXP_MIN", 10))
    JWT_REFRESH_TOKEN_EXP_DAY = int(os.environ.get("JWT_REFRESH_TOKEN_EXP_DAY", 7))
    TOPIC_ARN = os.environ.get("TOPIC_ARN")