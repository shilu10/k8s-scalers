import os 


class Config:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
    RABBITMQ_QUEUE_NAME = os.environ["RABBITMQ_QUEUE_NAME"]
    DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]
    DEEPGRAM_WS_URL = os.environ["DEEPGRAM_WS_URL"]

    AWS_REGION = os.environ["AWS_REGION"]
    MONGO_URI = os.environ.get("MONGO_URI")



