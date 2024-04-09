import os 


class Config:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_QUEUE_NAME = os.environ.get("RABBITMQ_QUEUE_NAME", "stress")
    REDIS_DB = int(os.environ.get("REDIS_DB", 0))