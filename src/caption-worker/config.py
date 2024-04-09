import os 


class Config:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    REDIS_DB = os.environ.get("REDIS_DB", 0)
    RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
    RABBITMQ_QUEUE_NAME = os.environ["RABBITMQ_QUEUE_NAME"]
    DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]
    DEEPGRAM_WS_URL = os.environ["DEEPGRAM_WS_URL"]


