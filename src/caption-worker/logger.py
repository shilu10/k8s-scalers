import logging
from logging.handlers import RotatingFileHandler


def setup_rotating_logger(name="deepgram_stream", log_file="deepgram_stream.log", max_bytes=1_000_000, backup_count=5):
    """
    Create a rotating logger that rolls over when the file reaches `max_bytes`.
    Keeps up to `backup_count` old log files.
    """
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")

    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers
    if not logger.handlers:
        # Rotating file handler
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
