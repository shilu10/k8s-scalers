import os 

class Config:
    NAMESPACE = os.environ.get("NAMESPACE", "dev")
    LABEL_SELECTOR = os.environ.get("LABEL_SELECTOR", "env=dev")
    ENDPOINT = os.environ.get("ENDPOINT", "/api/v1/stress")
    PORT = int(os.environ.get("PORT", 8001))

    LOAD = int(os.environ.get("LOAD"))
    DURATION = int(os.environ.get("DURATION"))
    WORKERS = int(os.environ.get("WORKERS"))
    STRESS_TYPE = os.environ.get("STRESS_TYPE")
    MEM_BYTES = int(os.environ.get("MEM_BYTES"))