# log.py
"""
Structured daily logging with rotation and error resilience.
"""
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from config import LOG_DIR

def get_logger() -> logging.Logger:
    logger = logging.getLogger("TicketingApp")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now():%Y%m%d}.txt"
    handler = RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

log = get_logger()

def log_action(action: str, ticket) -> None:
    entry = (
        f"{action} - {ticket.ticket_number} - \"{ticket.status}\" - "
        f"{ticket.description} - {ticket.username} - {ticket.created_date} - {ticket.updated_date}"
    )
    try:
        log.info(entry)
    except Exception as e:
        print(f"LOG-E01: Failed to log: {e}")