import os 


class BaseConfig:
    video_directory = "uploads"
    aws_access_key = os.environ["ACCESS_KEY"]
    aws_secret_access_key = os.environ["SECRET_ACCESS_KEY"]