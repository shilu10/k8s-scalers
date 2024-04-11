import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(app):
    log_dir = app.config.get("LOG_DIR")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # Set the logging level
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Debug statement
    print(f"Logging level set to {log_level}")
    
    # File handler
    log_file = os.path.join(log_dir, 'app.log')
    print(f"Log file path: {log_file}")
    
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Console Handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # Debug statement to show handlers
    for handler in app.logger.handlers:
        print(f"Handler: {handler}")


