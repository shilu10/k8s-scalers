import os 


class Config:
    video_directory = "uploads"
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PORT = os.environ["REDIS_PORT"]
    OBJECT_STORE_BUCKET_NAME = os.environ["OBJECT_STORE_BUCKET_NAME"]
    RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
    RABBITMQ_QUEUE_NAME = os.environ["RABBITMQ_QUEUE_NAME"]
    S3_REGION = os.environ["S3_REGION"]
