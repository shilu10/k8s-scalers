import os 


class Config:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_QUEUE_NAME = os.environ.get("RABBITMQ_QUEUE_NAME", "stress")
    REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB", "stress_app")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "transcripts")
    LOG_DIR = os.environ.get("LOG_DIR", "logs")