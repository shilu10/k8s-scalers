import os 


class Config:
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    MQ_QUEUE_NAME = os.environ["MQ_QUEUE_NAME"]
    DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]
    DEEPGRAM_WS_URL = os.environ.get("DEEPGRAM_WS_URL", "wss://api.deepgram.com/v1/listen?punctuate=true")

    MQ_USERNAME = os.environ.get("MQ_USERNAME", "xxxx")
    MQ_BROKER_ID = os.environ.get("MQ_BROKER_ID", "xxx")
    MQ_PASSWORD = os.environ.get("MQ_PASSWORD", "xxxx")
    MQ_ENDPOINT_SUFFIX = os.environ.get("MQ_ENDPOINT_SUFFIX", "mq.us-east-1.on.aws")

    AWS_REGION = os.environ["AWS_REGION"]
    MONGO_URI = os.environ.get("MONGO_URI")



