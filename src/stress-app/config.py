import os 

class Config:
    NAMESPACE = os.environ.get("NAMESPACE", "dev")
    LABEL_SELECTOR = os.environ.get("LABEL_SELECTOR", "env=dev")
    ENDPOINT = os.environ.get("ENDPOINT", "/api/v1/stress")
    PORT = os.environ.get("PORT", 8001)

    LOAD = os.environ.get("LOAD")
    DURATION = os.environ.get("DURATION")
    WORKERS = os.environ.get("WORKERS")
    STRESS_TYPE = os.environ.get("STRESS_TYPE")
    MEM_BYTES = os.environ.get("MEM_BYTES")