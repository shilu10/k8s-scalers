import os 


class Config:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    MQ_BROKER_ID = os.environ.get("MQ_BROKER_ID", "rabbitmq")
    MQ_USERNAME = os.environ.get("MQ_USERNAME", "shilash")
    MQ_PASSWORD = os.environ.get("MQ_PASSWORD", "password")
    REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB", "stress_app")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "transcripts")
    LOG_DIR = os.environ.get("LOG_DIR", "logs")