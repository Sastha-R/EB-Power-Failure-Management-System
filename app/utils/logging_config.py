import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR: str = "logs"

LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging() -> None:

    os.makedirs(LOG_DIR, exist_ok=True)

    root_logger: logging.Logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if getattr(root_logger, "_eb_logging_configured", False):
        return

    formatter: logging.Formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler: RotatingFileHandler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    root_logger._eb_logging_configured = True
