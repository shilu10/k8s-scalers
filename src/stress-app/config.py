import os
import logging

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class Config:
    try:
        NAMESPACE = os.environ.get("NAMESPACE", "dev")
        LABEL_SELECTOR = os.environ.get("LABEL_SELECTOR", "app.kubernetes.io/name=auth-service")
        ENDPOINT = os.environ.get("ENDPOINT", "/api/v1/stress")
        PORT = int(os.environ.get("PORT", 8001))

        # Required fields
        LOAD = int(os.environ["LOAD"])
        DURATION = int(os.environ["DURATION"])
        WORKERS = int(os.environ["WORKERS"])
        VM_WORKERS = int(os.environ["VM_WORKERS"])
        STRESS_TYPE = os.environ["STRESS_TYPE"]
        MEM_BYTES = int(os.environ["MEM_BYTES"])

        logger.debug("Successfully loaded all configuration values.")

    except KeyError as e:
        logger.error(f"Missing required environment variable: {e}")
        raise ValueError(f"Missing required environment variable: {e}")

    except ValueError as e:
        logger.error(f"Invalid value in environment variable: {e}")
        raise
