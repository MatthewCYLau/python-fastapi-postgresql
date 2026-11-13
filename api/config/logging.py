from datetime import datetime, timezone
import json
import logging
import sys


class SimpleJSONFormatter(logging.Formatter):
    """A minimal JSON formatter that captures standard info and optional user_id."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "severity": record.levelname,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id

        return json.dumps(log_record)


def setup_logging() -> None:
    """Set up simple structured JSON logging configuration."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(SimpleJSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]

    logging.getLogger("passlib").setLevel(logging.ERROR)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
