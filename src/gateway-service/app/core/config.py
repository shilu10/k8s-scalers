import os 


class Config:
    AUTH_SERVICE = os.environ.get("AUTH_SERVICE", "auth-service")
    UPLOAD_SERVICE = os.environ.get("UPLOAD_SERVICE", "upload-service")
    CAPTION_SERVICE = os.environ.get("CAPTION_SERVICE", "caption-service")

    AUTH_SERVICE_PORT = int(os.environ.get("AUTH_SERVICE_PORT", 8001))
    UPLOAD_SERVICE_PORT = int(os.environ.get("UPLOAD_SERVICE_PORT", 8002))
    CAPTION_SERVICE_PORT = int(os.environ.get("CAPTION_SERVICE_PORT", 8003))

    LOG_DIR = os.environ.get("LOG_DIR", "logs/")
